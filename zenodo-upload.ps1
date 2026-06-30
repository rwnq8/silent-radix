# ZENODO UPLOAD SCRIPT — Silent Radix Research Program v1.0
# Execute after setting ZENODO_TOKEN environment variable
# Usage: $env:ZENODO_TOKEN="your-token"; .\zenodo-upload.ps1

$ErrorActionPreference = "Stop"
$ZENODO_TOKEN = $env:ZENODO_TOKEN
if (-not $ZENODO_TOKEN) {
    Write-Error "[BLOCKED] ZENODO_TOKEN environment variable not set. Obtain at https://zenodo.org/account/settings/applications/"
    exit 1
}

$BASE_URL = "https://zenodo.org/api"
$HEADERS = @{
    "Authorization" = "Bearer $ZENODO_TOKEN"
    "Content-Type" = "application/json"
}

Write-Output "=== SILENT RADIX — Zenodo Publication v1.0 ==="
Write-Output ""

# Step 1: Create deposition
Write-Output "[1/4] Creating deposition..."
$metadata = Get-Content "zenodo-metadata.json" -Raw | ConvertFrom-Json
$body = $metadata | ConvertTo-Json -Depth 10
$response = Invoke-RestMethod -Uri "$BASE_URL/deposit/depositions" -Method Post -Headers $HEADERS -Body $body
$deposition_id = $response.id
$bucket_url = $response.links.bucket
Write-Output "  Deposition ID: $deposition_id"
Write-Output "  Bucket URL: $bucket_url"

# Step 2: Upload artifacts
Write-Output "[2/4] Uploading artifacts..."
$manifest = Get-Content "publication-manifest.json" -Raw | ConvertFrom-Json
foreach ($artifact in $manifest.artifacts) {
    $file = $artifact.file
    if (-not (Test-Path $file)) {
        Write-Output "  [SKIP] $file — not found"
        continue
    }
    $upload_url = "$bucket_url/$file"
    Write-Output "  Uploading: $file -> $upload_url"
    Invoke-RestMethod -Uri $upload_url -Method Put -Headers @{
        "Authorization" = "Bearer $ZENODO_TOKEN"
    } -InFile $file -ContentType "application/octet-stream"
}
Write-Output "  All artifacts uploaded."

# Step 3: Add version tag metadata
Write-Output "[3/4] Finalizing metadata..."
$version_metadata = @{
    metadata = @{
        version = "1.0.0"
        publication_date = "2026-06-29"
    }
} | ConvertTo-Json
Invoke-RestMethod -Uri "$BASE_URL/deposit/depositions/$deposition_id" -Method Put -Headers $HEADERS -Body $version_metadata

# Step 4: Publish
Write-Output "[4/4] Publishing deposition..."
$publish_response = Invoke-RestMethod -Uri "$BASE_URL/deposit/depositions/$deposition_id/actions/publish" -Method Post -Headers $HEADERS
$doi = $publish_response.doi
$conceptdoi = $publish_response.conceptdoi
$record_url = $publish_response.links.record

Write-Output ""
Write-Output "=== PUBLICATION COMPLETE ==="
Write-Output "  DOI: $doi"
Write-Output "  Concept DOI: $conceptdoi"
Write-Output "  Record URL: $record_url"
Write-Output "  Deposition ID: $deposition_id"
Write-Output ""
Write-Output "Next: Set env var SLT_RADIX_DOI=$doi for Buffer social posts."
