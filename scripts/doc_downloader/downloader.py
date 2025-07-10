#!/usr/bin/env python3
"""A Red Hat documentation downloader.

Downloads HTML pages from a given starting URL, preserving the directory structure.
"""

import argparse
import asyncio
import datetime
import json
import logging
import sqlite3
import sys
import time
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- URL Handling ---

def normalize_url(url: str) -> str:
    """Normalize a URL by removing fragment identifiers and query parameters."""
    parsed = urlparse(url)
    return parsed._replace(fragment="", query="").geturl()

def is_in_scope(url: str, base_url: str) -> bool:
    """Check if a URL is within the same domain and path as the base URL."""
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    if parsed_url.netloc != parsed_base_url.netloc:
        return False
    return parsed_url.path.startswith(parsed_base_url.path.rsplit('/', 1)[0])

def get_local_path(url: str, output_dir: Path, base_url: Optional[str] = None) -> Path:
    """Convert a URL to a local file path."""
    parsed_url = urlparse(url)
    path = parsed_url.path

    if base_url:
        parsed_base_url = urlparse(base_url)
        base_path = parsed_base_url.path
        # If base_url is a directory-like path, ensure it ends with a slash for clean prefix removal
        if not base_path.endswith('/') and '.' not in base_path.split('/')[-1]:
            base_path += '/'

        if path.startswith(base_path):
            path = path[len(base_path):]

    path = path.lstrip("/")

    if not path or path.endswith('/'):
        path = path + "index.html"
    
    local_path = output_dir / path
    local_path.parent.mkdir(parents=True, exist_ok=True)
    return local_path

# --- Database Functions ---

def init_database(db_path: str) -> str:
    """Initialize SQLite database."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            local_path TEXT NOT NULL,
            status TEXT NOT NULL,
            etag TEXT,
            last_modified TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
        conn.commit()
    logger.info("Database initialized at %s", db_path)
    return db_path

def record_download(
    db_path: str,
    url: str,
    local_path: str,
    status: str = "success",
    etag: Optional[str] = None,
    last_modified: Optional[str] = None,
):
    """Record a download in the database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO downloads (url, local_path, status, etag, last_modified, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))",
            (url, str(local_path), status, etag, last_modified),
        )
        conn.commit()

def get_download_status(db_path: str, url: str) -> tuple:
    """Get download status from database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT etag, last_modified FROM downloads WHERE url = ? AND status = 'success'",
            (url,),
        )
        result = cursor.fetchone()
    return result or (None, None)

# --- Network Functions ---

async def fetch_page(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Optional[str]:
    """Fetch a single page."""
    try:
        async with semaphore:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                logger.warning("Failed to fetch %s: HTTP %s", url, response.status)
                return None
    except Exception as e:
        logger.error("Error fetching %s: %s", url, e)
        return None

async def download_page(
    session: aiohttp.ClientSession,
    url: str,
    output_dir: Path,
    db_path: str,
    semaphore: asyncio.Semaphore,
    force: bool,
    max_retries: int,
    base_url: str,
) -> tuple[str, bool]:
    """Download a single page and save it."""
    local_path = get_local_path(url, output_dir, base_url)
    
    for attempt in range(max_retries):
        try:
            async with semaphore:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        with open(local_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        record_download(db_path, url, str(local_path))
                        logger.info("Downloaded %s -> %s", url, local_path)
                        return url, True
                    else:
                        logger.warning("Failed to download %s: HTTP %s", url, response.status)
                        if response.status == 404:
                            break # Don't retry on 404
        except Exception as e:
            logger.error("Error downloading %s: %s", url, e)
        
        if attempt < max_retries - 1:
            await asyncio.sleep(1)

    record_download(db_path, url, str(local_path), status="failed")
    return url, False

async def extract_links(
    session: aiohttp.ClientSession,
    url: str,
    base_url: str,
    visited_urls: set,
    semaphore: asyncio.Semaphore,
) -> set:
    """Extract all in-scope links from a page."""
    content = await fetch_page(session, url, semaphore)
    if not content:
        return set()

    soup = BeautifulSoup(content, "html.parser")
    new_links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        absolute_url = normalize_url(urljoin(url, href))
        
        if absolute_url not in visited_urls and is_in_scope(absolute_url, base_url):
            new_links.add(absolute_url)
            
    return new_links

async def crawl(session: aiohttp.ClientSession, start_url: str, semaphore: asyncio.Semaphore) -> set:
    """Crawl a website to discover all pages."""
    base_url = normalize_url(start_url)
    to_visit = {base_url}
    visited_urls = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited_urls:
            continue
        
        visited_urls.add(url)
        logger.debug("Crawling %s", url)
        
        new_links = await extract_links(session, url, base_url, visited_urls, semaphore)
        to_visit.update(new_links)

    # Heuristic: if the start_url doesn't look like a document page, don't include it for download.
    # Document pages usually end in .html or are in a /html-single/ directory.
    parsed_start_url = urlparse(base_url)
    if not parsed_start_url.path.endswith('.html') and '/html-single/' not in parsed_start_url.path:
         if base_url in visited_urls:
            logger.info("Excluding dispatch page from download list: %s", base_url)
            visited_urls.remove(base_url)

    logger.info("Crawling completed. Found %s pages.", len(visited_urls))
    return visited_urls

# --- Main Execution ---

async def run_downloader(
    base_url: str,
    output_dir: Union[str, Path],
    concurrency: int,
    force: bool,
    max_retries: int,
    **kwargs, # Absorb unused arguments
) -> tuple[bool, bool, float]:
    """Run the complete download process."""
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)
    db_path = str(output_dir_path / "download_database.sqlite")
    init_database(db_path)
    
    semaphore = asyncio.Semaphore(concurrency)
    start_time = time.time()

    async with aiohttp.ClientSession(trust_env=True) as session:
        discovered_urls = await crawl(session, base_url, semaphore)
        
        tasks = [
            download_page(session, url, output_dir_path, db_path, semaphore, force, max_retries, base_url)
            for url in discovered_urls
        ]
        results = await asyncio.gather(*tasks)

    successful_downloads = sum(1 for _, success in results if success)
    elapsed_time = time.time() - start_time
    
    logger.info(
        "Download process completed in %.2f seconds. %s/%s pages downloaded successfully.",
        elapsed_time,
        successful_downloads,
        len(discovered_urls),
    )
    
    return successful_downloads > 0, True, elapsed_time

def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Download documentation from a URL.")
    parser.add_argument("--doc-url", required=True, help="The starting URL to crawl.")
    parser.add_argument("--output-dir", required=True, help="Directory to save files.")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrency level.")
    parser.add_argument("--force", action="store_true", help="Force re-download of all files.")
    parser.add_argument("--max-retries", type=int, default=3, help="Max retries for failed downloads.")
    args = parser.parse_args()

    asyncio.run(run_downloader(
        base_url=args.doc_url,
        output_dir=args.output_dir,
        concurrency=args.concurrency,
        force=args.force,
        max_retries=args.max_retries,
    ))

if __name__ == "__main__":
    main()
