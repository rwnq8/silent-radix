# BUFFER SOCIAL MEDIA SCHEDULE SCRIPT — Silent Radix Research Program v1.0
# Posts to Twitter, LinkedIn, Mastodon, and Bluesky via Buffer API
# Requires: BUFFER_ACCESS_TOKEN environment variable
# Usage: $env:BUFFER_ACCESS_TOKEN="your-token"; $env:SLT_RADIX_DOI="10.5281/zenodo.XXXXX"; .\buffer-schedule.ps1

$ErrorActionPreference = "Stop"
$BUFFER_TOKEN = $env:BUFFER_ACCESS_TOKEN
$DOI = $env:SLT_RADIX_DOI

if (-not $BUFFER_TOKEN) {
    Write-Error "[BLOCKED] BUFFER_ACCESS_TOKEN env var not set. Obtain at https://buffer.com/developers/api"
    exit 1
}
if (-not $DOI) {
    Write-Warning "[WARN] SLT_RADIX_DOI not set. Using placeholder in posts. Set after Zenodo publication."
    $DOI = "10.5281/zenodo.XXXXX (pending)"
}

Write-Output "=== SILENT RADIX — Buffer Social Media Schedule ==="
Write-Output "DOI: $DOI"
Write-Output ""

$posts = Get-Content "buffer-social-posts.json" -Raw | ConvertFrom-Json
$BUFFER_API = "https://api.bufferapp.com/1/updates/create.json"
$HEADERS = @{
    "Authorization" = "Bearer $BUFFER_TOKEN"
    "Content-Type" = "application/x-www-form-urlencoded"
}

# Map platform names to Buffer profile IDs (REPLACE with actual profile IDs)
$PROFILE_IDS = @{
    "twitter" = "[YOUR_TWITTER_PROFILE_ID]"
    "linkedin" = "[YOUR_LINKEDIN_PROFILE_ID]"
    "mastodon" = "[YOUR_MASTODON_PROFILE_ID]"
    "bluesky" = "[YOUR_BLUESKY_PROFILE_ID]"
}

$count = 0
foreach ($post in $posts.social_posts) {
    $count++
    $text = $post.text -replace '\[SLT_RADIX_DOI\]', $DOI
    $platform = $post.platform
    $profile_id = $PROFILE_IDS[$platform]

    if ($profile_id -match '^\[YOUR_') {
        Write-Output "[$count/$($posts.social_posts.Count)] [SKIP] $platform — profile ID not configured"
        continue
    }

    $body = @{
        "text" = $text
        "profile_ids[]" = $profile_id
        "shorten" = "true"
        "now" = if ($post.scheduled_at) { "false" } else { "true" }
    }

    if ($post.scheduled_at -and $post.scheduled_at -ne "null") {
        $body["scheduled_at"] = $post.scheduled_at
    }

    Write-Output "[$count/$($posts.social_posts.Count)] Posting to $platform..."
    Write-Output "  Text: $($text.Substring(0, [Math]::Min(80, $text.Length)))..."

    $formBody = ($body.GetEnumerator() | ForEach-Object {
        "$($_.Key)=$([System.Web.HttpUtility]::UrlEncode($_.Value))"
    }) -join "&"

    try {
        $response = Invoke-RestMethod -Uri $BUFFER_API -Method Post -Headers $HEADERS -Body $formBody
        Write-Output "  [OK] Posted. Buffer ID: $($response.id)"
    } catch {
        Write-Error "  [FAIL] $_"
    }
}

Write-Output ""
Write-Output "=== SCHEDULE COMPLETE ==="
Write-Output "  Posts scheduled: $count"
Write-Output "  Platforms: $($posts.social_posts | ForEach-Object { $_.platform } | Select-Object -Unique)"
Write-Output "  Strategy: $($posts.thread.schedule_strategy)"
Write-Output "  Interval: $($posts.thread.interval)"
Write-Output ""
Write-Output "Verify at: https://buffer.com/app"
