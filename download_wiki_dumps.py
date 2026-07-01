#!/usr/bin/env python3
"""
Wikipedia dump downloader for UVR Pipeline.
Downloads the 4 required SQL dump files from dumps.wikimedia.org.

Usage: python download_wiki_dumps.py --output-dir ./enwiki-dump/ [--latest]
"""

import argparse
import urllib.request
import sys
import os
import re
from pathlib import Path

DUMP_FILES = [
    'page.sql.gz',
    'categorylinks.sql.gz',
    'pagelinks.sql.gz',
    'category.sql.gz',
]

def get_latest_date():
    """Find the latest available Wikipedia dump date."""
    url = 'https://dumps.wikimedia.org/enwiki/'
    req = urllib.request.Request(url, headers={'User-Agent': 'QNFO-UVR/1.0'})
    resp = urllib.request.urlopen(req, timeout=30)
    html = resp.read().decode('utf-8')
    dates = re.findall(r'href="(\d{8})/', html)
    dates = sorted(set(dates), reverse=True)
    return dates[0] if dates else None

def download_file(url, dest_path, retries=3):
    """Download a file with retry logic."""
    for attempt in range(retries):
        try:
            print(f"  Downloading {url} ...", end=' ', flush=True)
            req = urllib.request.Request(url, headers={'User-Agent': 'QNFO-UVR/1.0'})
            resp = urllib.request.urlopen(req, timeout=300)
            total = int(resp.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1 MB
            with open(dest_path, 'wb') as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = downloaded / total * 100
                        print(f"\r  {pct:.0f}%", end='', flush=True)
            print(f" [DONE]")
            return True
        except Exception as e:
            print(f" [FAILED: {e}]")
            if attempt < retries - 1:
                print(f"  Retrying ({attempt + 2}/{retries})...")
    return False

def main():
    parser = argparse.ArgumentParser(description='Download Wikipedia SQL dumps for UVR pipeline')
    parser.add_argument('--output-dir', '-o', required=True, help='Output directory for dump files')
    parser.add_argument('--date', '-d', help='Wikipedia dump date (YYYYMMDD), default: latest')
    args = parser.parse_args()

    if args.date:
        dump_date = args.date
    else:
        dump_date = get_latest_date()
        if not dump_date:
            print("ERROR: Could not determine latest dump date")
            sys.exit(1)

    print(f"Wikipedia dump date: {dump_date}")
    base_url = f'https://dumps.wikimedia.org/enwiki/{dump_date}/'
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for dump_file in DUMP_FILES:
        filename = f'enwiki-{dump_date}-{dump_file}'
        url = f'{base_url}{filename}'
        dest = output_dir / filename
        if dest.exists():
            size_mb = dest.stat().st_size / (1024*1024)
            print(f"  [SKIP] {filename} already exists ({size_mb:.0f} MB)")
            continue
        
        success = download_file(url, dest)
        if not success:
            print(f"  [FAILED] {filename} could not be downloaded")
            sys.exit(1)

    print(f"\nAll dumps downloaded to: {output_dir}")
    print(f"Run pipeline: python wikipedia_uvr_pipeline.py --dump-dir {output_dir} --sample 50000")

if __name__ == '__main__':
    main()
