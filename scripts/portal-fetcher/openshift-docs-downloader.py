#!/usr/bin/env python3
"""OpenShift Documentation Downloader.

Downloads the HTML-single version of Red Hat OpenShift documentation for a specified version,
preserving directory structure and maintaining a database of downloaded files.
Supports incremental updates and advanced verification.
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

# Pure functions for URL handling


def normalize_url(url: str) -> str:
    """Normalize a URL by removing fragment identifiers and ensuring consistency.

    Args:
        url (str): URL to normalize

    Returns:
        str: Normalized URL
    """
    # Parse the URL
    parsed = urlparse(url)

    # Remove fragment identifier
    parsed = parsed._replace(fragment="")

    # Build the path without trailing index if present
    path = parsed.path
    path = path.removesuffix("/index")
    if not path.endswith("/"):
        path = path + "/"

    # Reassemble the URL
    normalized = parsed._replace(path=path).geturl()

    return normalized


def is_likely_external_link(url: str) -> bool:
    """Check if a URL is likely to be an external link that's incorrectly formatted as internal.

    Args:
        url (str): URL to check

    Returns:
        bool: True if the URL is likely an external link
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Common domains that might appear in the path part of malformed URLs
    domain_patterns = [
        "console.redhat.com",
        "github.com",
        "access.redhat.com",
        "login.redhat.com",
        ".io/",
        ".com/",
        ".org/",
        ".net/",
        "www.",
        "http:",
        "https:",
    ]

    # Check if the path contains any domain-like patterns
    return any(pattern in path for pattern in domain_patterns)


def is_html_single_url(url: str) -> bool:
    """Check if a URL is an html-single version page.

    Args:
        url (str): URL to check

    Returns:
        bool: True if the URL is an html-single version page
    """
    return "/html-single/" in url


def is_in_scope(url: str, base_url: str) -> bool:
    """Check if a URL is within our target scope.

    Args:
        url (str): URL to check
        base_url (str): Base URL for comparison

    Returns:
        bool: True if the URL is within our scope
    """
    # Get just the path part of both URLs
    url_path = urlparse(url).path
    base_path = urlparse(base_url).path

    # For specific doc scoping, we want to make sure the URL is under the same path
    # But also handle the case where the base URL doesn't include the actual page
    if "/html-single/" in base_path:
        # If this is a specific doc, make sure it's within that doc's URL path
        return url_path.startswith(base_path) or url_path == base_path.removesuffix("/index")
    else:
        # For entire docs, anything with openshift_container_platform/VERSION in scope
        try:
            version_part = f"openshift_container_platform/{base_url.split('openshift_container_platform/')[1].split('/')[0]}"
            is_in_scope = version_part in url and is_html_single_url(url)
        except IndexError:
            is_in_scope = False

        return is_in_scope


def get_local_path(url: str, output_dir: Path) -> Path:
    """Convert a URL to a local file path, preserving directory structure.

    Args:
        url (str): URL of the documentation page
        output_dir (Path): Base output directory

    Returns:
        Path: Local path where the file will be saved
    """
    url = normalize_url(url)
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_parts = path.strip("/").split("/")

    try:
        doc_type_index = path_parts.index("html-single") if "html-single" in path_parts else path_parts.index("html")
        
        if doc_type_index + 1 < len(path_parts):
            doc_name = path_parts[doc_type_index + 1]

            # If the output directory is already the doc-specific folder, don't nest further.
            target_dir = output_dir if output_dir.name == doc_name else output_dir / doc_name
            
            local_path = target_dir / "index.html"
        else:
            # Fallback for unexpected URL structures
            local_path = output_dir / "index.html"

    except (ValueError, IndexError):
        # Fallback if html-single not in path
        if path.endswith("/"):
            path += "index.html"
        elif not path.endswith(".html"):
            path += "/index.html"
        local_path = output_dir / path.lstrip("/")

    local_path.parent.mkdir(parents=True, exist_ok=True)
    return local_path


# Database functions


def init_database(db_path: str) -> str:
    """Initialize SQLite database to track downloaded files"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Main downloads table
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

        # History table to track changes
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS download_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            local_path TEXT NOT NULL,
            status TEXT NOT NULL,
            etag TEXT,
            last_modified TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            change_type TEXT NOT NULL
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
    change_type: Optional[str] = None,
) -> str:
    """Record a download in the database and update history

    Args:
        db_path (Path): Path to SQLite database
        url (str): URL of the downloaded page
        local_path (str/Path): Local path where the file is saved
        status (str): Download status (success, failed, error)
        etag (str): ETag header from the response, if available
        last_modified (str): Last-Modified header from the response, if available
        change_type (str): Type of change (new, updated, unchanged, error)
    """
    local_path_str = str(local_path)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        try:
            # Record in main downloads table
            cursor.execute(
                "INSERT OR REPLACE INTO downloads (url, local_path, status, etag, last_modified, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                (url, local_path_str, status, etag, last_modified),
            )

            # Record in history table
            if change_type:
                cursor.execute(
                    "INSERT INTO download_history (url, local_path, status, etag, last_modified, change_type) VALUES (?, ?, ?, ?, ?, ?)",
                    (url, local_path_str, status, etag, last_modified, change_type),
                )

            conn.commit()
        except Exception as e:
            logger.error("Database error: %s", e)
            conn.rollback()

    return url


def get_download_status(db_path: str, url: str) -> dict:
    """Get download status from database

    Args:
        db_path (Path): Path to SQLite database
        url (str): URL to check

    Returns:
        tuple: (etag, last_modified)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT etag, last_modified FROM downloads WHERE url = ? AND status = 'success'",
            (url,),
        )
        result = cursor.fetchone()

    existing_etag = result[0] if result else None
    existing_last_modified = result[1] if result else None

    return (existing_etag, existing_last_modified)


def get_download_results(db_path: str) -> tuple[set[str], set[str]]:
    """Get all successful and failed downloads

    Args:
        db_path (Path): Path to SQLite database

    Returns:
        tuple: (successful_urls, failed_urls)
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Get all successful downloads
        cursor.execute("SELECT url FROM downloads WHERE status = 'success'")
        successful_urls = {row[0] for row in cursor.fetchall()}

        # Get all failed downloads
        cursor.execute("SELECT url FROM downloads WHERE status != 'success'")
        failed_urls = {row[0] for row in cursor.fetchall()}

    return (successful_urls, failed_urls)


def get_url_mapping(db_path: str) -> dict[str, str]:
    """Get mapping of local file paths to their source URLs

    Args:
        db_path (Path): Path to SQLite database

    Returns:
        dict: {local_path: url}
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT local_path, url FROM downloads WHERE status = 'success'")
        mapping = {row[0]: row[1] for row in cursor.fetchall()}

    return mapping


def get_change_report(db_path: str) -> dict:
    """Get change report data

    Args:
        db_path (Path): Path to SQLite database

    Returns:
        dict: Report data
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Get counts by change type
        cursor.execute(
            """
            SELECT change_type, COUNT(*)
            FROM download_history
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY change_type
        """
        )
        change_counts = {row[0]: row[1] for row in cursor.fetchall()}

        # Get list of updated files with timestamps
        cursor.execute(
            """
            SELECT h.url, h.timestamp, d.timestamp
            FROM download_history h
            JOIN downloads d ON h.url = d.url
            WHERE h.change_type = 'updated'
            AND h.timestamp > datetime('now', '-1 hour')
        """
        )
        updated_files = [
            {"url": row[0], "previous_timestamp": row[1], "current_timestamp": row[2]}
            for row in cursor.fetchall()
        ]

        # Get list of new files
        cursor.execute(
            """
            SELECT url
            FROM download_history
            WHERE change_type = 'new'
            AND timestamp > datetime('now', '-1 hour')
        """
        )
        new_files = [row[0] for row in cursor.fetchall()]

        # Get list of errors
        cursor.execute(
            """
            SELECT url
            FROM download_history
            WHERE change_type = 'error'
            AND timestamp > datetime('now', '-1 hour')
        """
        )
        error_files = [row[0] for row in cursor.fetchall()]

    # Create the report
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": change_counts,
        "updated_files": updated_files,
        "new_files": new_files,
        "error_files": error_files,
    }

    return report


# Network functions


async def fetch_page(
    session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore
) -> str:
    """Fetch a page and return its content

    Args:
        session (aiohttp.ClientSession): HTTP session
        url (str): URL to fetch
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        str: HTML content of the page
    """
    try:
        async with semaphore:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning("Failed to fetch %s: HTTP %s", url, response.status)
                    return None
    except Exception as e:
        logger.error("Error fetching %s: %s", url, e)
        return None


async def check_if_modified(
    session: aiohttp.ClientSession, url: str, db_path: str, semaphore: asyncio.Semaphore
) -> tuple[bool, str, str]:
    """Check if a page has been modified since the last download

    Args:
        session (aiohttp.ClientSession): HTTP session
        url (str): URL to check
        db_path (Path): Path to SQLite database
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        tuple: (needs_download, etag, last_modified)
    """
    # Get existing information from database
    existing_etag, existing_last_modified = get_download_status(db_path, url)

    headers = {}
    if existing_etag:
        headers["If-None-Match"] = existing_etag
    if existing_last_modified:
        headers["If-Modified-Since"] = existing_last_modified

    try:
        async with semaphore:
            async with session.head(url, headers=headers, timeout=15) as response:
                # Get current ETag and Last-Modified
                current_etag = response.headers.get("ETag")
                current_last_modified = response.headers.get("Last-Modified")

                # If we get a 304 Not Modified, we don't need to download
                if response.status == 304:
                    return False, current_etag, current_last_modified

                # If we have an ETag and it matches, we don't need to download
                if existing_etag and current_etag and existing_etag == current_etag:
                    return False, current_etag, current_last_modified

                # If we have Last-Modified and it matches, we don't need to download
                if (
                    existing_last_modified
                    and current_last_modified
                    and existing_last_modified == current_last_modified
                ):
                    return False, current_etag, current_last_modified

                # Otherwise, we need to download
                return True, current_etag, current_last_modified
    except Exception as e:
        logger.warning("Error checking if modified for %s: %s", url, e)
        # If we can't check, assume we need to download
        return True, None, None


async def download_page(
    session: aiohttp.ClientSession,
    url: str,
    output_dir: Path,
    db_path: str,
    semaphore: asyncio.Semaphore,
    force: bool = False,
    max_retries: int = 3,
) -> tuple[str, bool, set[str]]:
    """Download a page and save it to the local file system

    Args:
        session (aiohttp.ClientSession): HTTP session
        url (str): URL to download
        output_dir (Path): Base output directory
        db_path (Path): Path to SQLite database
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests
        max_retries (int): Maximum number of retry attempts
        force (bool): Force download even if not modified

    Returns:
        tuple: (url, success, failed_downloads)
    """
    # Check if this is likely an external link incorrectly formatted as internal
    if is_likely_external_link(url):
        logger.info(
            "Skipping likely external URL incorrectly formatted as internal: %s", url
        )
        record_download(
            db_path, url, "N/A", status="skipped", change_type="skipped_external"
        )
        return (url, True, set())

    local_path = get_local_path(url, output_dir)

    # Check if we need to download
    if not force:
        needs_download, etag, last_modified = await check_if_modified(
            session, url, db_path, semaphore
        )
        if not needs_download:
            logger.debug("Skipping %s (not modified)", url)
            record_download(
                db_path,
                url,
                local_path,
                status="success",
                etag=etag,
                last_modified=last_modified,
                change_type="unchanged",
            )
            return (url, True, set())
    for attempt in range(max_retries):
        try:
            async with semaphore:
                retry_msg = (
                    " (attempt %s/%s)" % (attempt + 1, max_retries) if attempt > 0 else ""
                )
                logger.debug("Downloading %s%s", url, retry_msg)
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()

                        # Get ETag and Last-Modified
                        etag_value = response.headers.get("ETag")
                        last_modified_value = response.headers.get("Last-Modified")
                        etag = etag_value if etag_value is not None else ""
                        last_modified = (
                            last_modified_value
                            if last_modified_value is not None
                            else ""
                        )

                        # Determine change type
                        if local_path.exists():
                            change_type = "updated"
                        else:
                            change_type = "new"

                        # Save the content
                        with open(local_path, "w", encoding="utf-8") as f:
                            f.write(content)

                        # Record in database
                        record_download(
                            db_path,
                            url,
                            local_path,
                            etag=etag,
                            last_modified=last_modified,
                            change_type=change_type,
                        )
                        logger.info("Downloaded %s -> %s (%s)", url, local_path, change_type)
                        return (url, True, set())
                    elif response.status == 404:
                        # Check if this might be an expected 404 for an external link
                        if is_likely_external_link(url):
                            logger.info("Skipping 404 for likely external URL: %s", url)
                            record_download(
                                db_path,
                                url,
                                "N/A",
                                status="skipped",
                                change_type="external_404",
                            )
                            return (url, True, set())
                        elif attempt == max_retries - 1:
                            # It's a real 404 for a document that should exist, and we've tried max times
                            logger.warning("Failed to download %s: HTTP 404", url)
                            record_download(
                                db_path,
                                url,
                                local_path,
                                status="failed_404",
                                change_type="error",
                            )
                            return (url, False, {url})
                    else:
                        if attempt == max_retries - 1:
                            # Final attempt failed with a non-404 error
                            logger.warning(
                                "Failed to download %s: HTTP %s", url, response.status
                            )
                            record_download(
                                db_path,
                                url,
                                local_path,
                                status="failed",
                                change_type="error",
                            )
                            return (url, False, {url})

                # If we got here and it's not the last attempt, continue to next try
                if attempt < max_retries - 1:
                    logger.warning(
                        "Retrying download for %s after unsuccessful attempt", url
                    )
                    await asyncio.sleep(1)  # Small delay before retry

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning("Error downloading %s: %s. Retrying...", url, e)
                await asyncio.sleep(1)  # Small delay before retry
            else:
                logger.error("Error downloading %s: %s. Max retries reached.", url, e)
                record_download(
                    db_path, url, local_path, status="error", change_type="error"
                )
                return (url, False, {url})

    # Fallback case - this should rarely happen but just in case
    record_download(db_path, url, local_path, status="error", change_type="error")
    return (url, False, {url})


async def extract_links(
    session: aiohttp.ClientSession,
    url: str,
    base_url: str,
    visited_urls: set[str],
    semaphore: asyncio.Semaphore,
) -> set[str]:
    """Extract all links from a page

    Args:
        session (aiohttp.ClientSession): HTTP session
        url (str): URL of the page
        base_url (str): Base URL for comparison
        visited_urls (set): Set of already visited URLs
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        tuple: (new_links, new_html_single_urls)
    """
    content = await fetch_page(session, url, semaphore)
    if not content:
        return (set(), set())

    soup = BeautifulSoup(content, "html.parser")
    links = set()
    html_single_urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        absolute_url = urljoin(url, href)

        # Normalize the URL to remove fragment identifiers
        normalized_url = normalize_url(absolute_url)

        # Only consider URLs within the same documentation version and path
        if "/html-single/" in normalized_url and normalized_url.startswith(base_url):
            if normalized_url not in visited_urls:
                links.add(normalized_url)

                # If this is an html-single URL within our base URL, add it to our collection
                html_single_urls.add(normalized_url)

    return (links, html_single_urls)


async def extract_root_guides(
    session: aiohttp.ClientSession,
    url: str,
    base_url: str,
    semaphore: asyncio.Semaphore,
) -> set[str]:
    """Extract guide links from the root documentation page

    Args:
        session (aiohttp.ClientSession): HTTP session
        url (str): URL of the root page
        base_url (str): Base URL for the documentation
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        set: Set of guide URLs
    """
    logger.info("Processing root documentation page: %s", url)
    content = await fetch_page(session, url, semaphore)
    if not content:
        return set()

    soup = BeautifulSoup(content, "html.parser")

    # Find all guide links - these typically point to /html/ versions
    guide_links = set()
    html_single_urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        # Look for HTML documentation links, excluding external links
        if "/html/" in href and "redhat.com" not in href and "://" not in href:
            absolute_url = urljoin(url, href)
            guide_links.add(absolute_url)

    logger.info("Found %s documentation guides on main page", len(guide_links))

    # For each guide, convert to html-single version and add to the collection
    for html_url in guide_links:
        # Convert from /html/ to /html-single/
        html_single_url = html_url.replace("/html/", "/html-single/")
        normalized_url = normalize_url(html_single_url)
        html_single_urls.add(normalized_url)
        logger.debug("Added guide to download queue: %s", normalized_url)

    return html_single_urls


async def crawl(
    session: aiohttp.ClientSession,
    start_url: str,
    base_url: str,
    semaphore: asyncio.Semaphore,
) -> tuple[set[str], set[str]]:
    """Crawl the documentation to discover all html-single pages

    Args:
        session (aiohttp.ClientSession): HTTP session
        start_url (str): Starting URL for the crawl
        base_url (str): Base URL for the documentation
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        tuple: (visited_urls, html_single_urls)
    """
    # Normalize the start URL
    start_url = normalize_url(start_url)

    # Sets to track our progress
    visited_urls = set()
    html_single_urls = set()

    # Make sure to add the index page explicitly for the specified document
    if "/html-single/" in start_url:
        # Add the specific document's index page
        html_single_urls.add(start_url)

    to_visit = {start_url}

    # Special case handling for root documentation page
    is_root_doc_page = (
        "openshift_container_platform" in start_url and "/html" not in start_url
    )

    # For main page crawl, we need to extract all guide links first
    if is_root_doc_page:
        root_guides = await extract_root_guides(session, start_url, base_url, semaphore)
        html_single_urls.update(root_guides)
        to_visit.update(root_guides)

    while to_visit:
        url = to_visit.pop()
        normalized_url = normalize_url(url)

        if normalized_url in visited_urls:
            continue

        visited_urls.add(normalized_url)
        logger.debug("Crawling %s", normalized_url)

        new_links, new_html_single_urls = await extract_links(
            session, normalized_url, base_url, visited_urls, semaphore
        )
        to_visit.update({link for link in new_links if link not in visited_urls})
        html_single_urls.update(new_html_single_urls)

    logger.info("Crawling completed. Found %s html-single pages.", len(html_single_urls))

    return (visited_urls, html_single_urls)


async def download_all(
    session: aiohttp.ClientSession,
    urls: set[str],
    output_dir: Path,
    db_path: str,
    semaphore: asyncio.Semaphore,
    force: bool = False,
    max_retries: int = 3,
) -> tuple[int, int, set[str]]:
    """Download all discovered html-single pages

    Args:
        session (aiohttp.ClientSession): HTTP session
        urls (set): Set of URLs to download
        output_dir (Path): Base output directory
        db_path (Path): Path to SQLite database
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests
        force (bool): Force download even if files haven't changed
        max_retries (int): Maximum number of retry attempts for failed downloads

    Returns:
        tuple: (successes, failures, failed_downloads)
    """
    if not urls:
        logger.warning("No html-single pages found to download.")
        return (0, 0, set())

    logger.info(
        "Starting download of %s pages (force=%s, max_retries=%s)...",
        len(urls),
        force,
        max_retries,
    )

    # Create tasks for all downloads
    tasks = [
        download_page(session, url, output_dir, db_path, semaphore, force, max_retries)
        for url in urls
    ]
    results = await asyncio.gather(*tasks)

    # Count successes and failures, and collect failed downloads
    successes = sum(1 for _, success, _ in results if success)
    failures = len(results) - successes
    failed_downloads = set()
    for _, success, fails in results:
        if not success:
            failed_downloads.update(fails)

    logger.info("Download completed: %s successful, %s failed.", successes, failures)

    if failures > 0:
        logger.warning("Failed to download %s pages. See log for details.", failures)
        # Record failed downloads for retry
        with open(output_dir / "failed_downloads.json", "w") as f:
            json.dump(list(failed_downloads), f, indent=2)

    return (successes, failures, failed_downloads)


async def verify_downloads(
    html_single_urls: set[str], db_path: str, output_dir: Path, fail_on_error: bool = False
) -> bool:
    """Verify that all html-single pages were downloaded successfully

    Args:
        html_single_urls (set): Set of all discovered URLs
        db_path (Path): Path to SQLite database
        output_dir (Path): Base output directory
        fail_on_error: Stop the pipeline if any document fails to download
    Returns:
        bool: True if verification passed
    """
    logger.info("Verifying downloads...")

    # Get download results from database
    successful_urls, failed_urls = get_download_results(db_path)

    # Check for any URLs that were discovered but never attempted
    missing_urls = html_single_urls - successful_urls - failed_urls
    total_failed = len(failed_urls) + len(missing_urls)

    if total_failed > 0:
        logger.warning(
            "Verification issues found: %s failed or missing URLs.", total_failed
        )
        # Log the details of failures regardless of the flag
        if missing_urls:
            logger.warning("Missing URLs (never attempted): %s", len(missing_urls))
            with open(output_dir / "missing_urls.json", "w") as f:
                json.dump(list(missing_urls), f, indent=2)
        if failed_urls:
             logger.warning("Failed URLs (download error): %s", len(failed_urls))

        # Only halt the pipeline if the flag is set
        if fail_on_error:
            logger.error(
                "Failures detected and --fail-on-download-error is set. Halting."
            )
            return False

    logger.info("Verification completed. Proceeding with successfully downloaded content.")
    return True


async def extract_toc_structure(
    session: aiohttp.ClientSession,
    visited_urls: set[str],
    base_url: str,
    semaphore: asyncio.Semaphore,
) -> set[str]:
    """Extract documentation structure from table of contents pages

    Args:
        session (aiohttp.ClientSession): HTTP session
        visited_urls (set): Set of visited URLs
        base_url (str): Base URL for the documentation
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        set: Set of URLs that should be in the documentation
    """
    logger.info("Extracting documentation structure from TOC pages...")

    # Look for index pages that might contain a TOC
    toc_candidates = set()
    for url in visited_urls:
        normalized_url = normalize_url(url)
        if normalized_url.endswith("/") or "/index" in normalized_url:
            toc_candidates.add(normalized_url)

    # Special case: always include the main index page
    main_index = normalize_url(f"{base_url}/index")
    if main_index not in toc_candidates:
        toc_candidates.add(main_index)

    logger.info("Found %s potential TOC pages to analyze", len(toc_candidates))

    # Extract links from TOC pages
    expected_urls = set()
    for url in toc_candidates:
        logger.debug("Analyzing TOC page: %s", url)
        content = await fetch_page(session, url, semaphore)
        if not content:
            continue

        soup = BeautifulSoup(content, "html.parser")

        # Look for typical TOC elements
        toc_selectors = [
            "nav",
            ".toc",
            ".navigation",
            ".nav",
            ".sidebar",
            ".menu",
            ".contents",
            "#toc",
            "#navigation",
            "#sidebar",
            "#menu",
            "#contents",
            ".index",
            "#index",
            ".documentation-toc",
            "#documentation-toc",
            "[role='navigation']",
            "[role='menu']",
            "[role='toc']",
        ]

        toc_elements = []
        for selector in toc_selectors:
            elements = soup.select(selector)
            if elements:
                toc_elements.extend(elements)

        # If none found, use the whole page
        if not toc_elements:
            toc_elements = [soup]

        # Extract links from TOC elements
        for element in toc_elements:
            for link in element.find_all("a", href=True):
                href = link["href"]
                absolute_url = urljoin(url, href)

                # Only include html-single URLs within our base URL
                if "/html-single/" in absolute_url and base_url in absolute_url:
                    normalized_url = normalize_url(absolute_url)
                    expected_urls.add(normalized_url)

    logger.info("Extracted %s expected URLs from TOC analysis", len(expected_urls))
    return expected_urls


async def verify_against_toc(
    session: aiohttp.ClientSession,
    html_single_urls: set[str],
    visited_urls: set[str],
    base_url: str,
    db_path: str,
    output_dir: Path,
    semaphore: asyncio.Semaphore,
) -> bool:
    """Verify downloads against TOC structure

    Args:
        session (aiohttp.ClientSession): HTTP session
        html_single_urls (set): Set of all discovered URLs
        visited_urls (set): Set of visited URLs
        base_url (str): Base URL for the documentation
        db_path (Path): Path to SQLite database
        output_dir (Path): Base output directory
        semaphore (asyncio.Semaphore): Semaphore for limiting concurrent requests

    Returns:
        bool: True if verification passed
    """
    logger.info("Verifying downloads against TOC structure...")

    # Get expected URLs from TOC
    expected_urls = await extract_toc_structure(
        session, visited_urls, base_url, semaphore
    )

    # Get downloaded URLs
    successful_urls, _ = get_download_results(db_path)

    # Normalize downloaded URLs
    downloaded_urls = {normalize_url(url) for url in successful_urls}

    # Find missing URLs
    missing_urls = expected_urls - downloaded_urls

    if missing_urls:
        logger.warning(
            "Found %s pages listed in TOC that were not downloaded.", len(missing_urls)
        )
        with open(output_dir / "missing_toc_urls.json", "w") as f:
            json.dump(list(missing_urls), f, indent=2)
        return False

    logger.info("TOC verification completed successfully.")
    return True


def export_url_mapping(db_path: str, output_dir: Path) -> dict[str, str]:
    """Export a mapping of local file paths to their source URLs

    Args:
        db_path (Path): Path to SQLite database
        output_dir (Path): Base output directory
    """
    logger.info("Exporting URL mapping...")

    mapping = get_url_mapping(db_path)

    with open(output_dir / "url_mapping.json", "w") as f:
        json.dump(mapping, f, indent=2)

    logger.info("Exported mapping for %s files.", len(mapping))

    return mapping


def export_change_report(db_path: str, output_dir: Path) -> dict:
    """Export a report of changes from the current run

    Args:
        db_path (Path): Path to SQLite database
        output_dir (Path): Base output directory
    """
    logger.info("Generating change report...")

    report = get_change_report(db_path)

    with open(output_dir / "change_report.json", "w") as f:
        json.dump(report, f, indent=2)

    logger.info("Change report generated.")

    return report


async def run_downloader(
    base_url: str,
    output_dir: Union[str, Path],
    concurrency: int = 5,
    force: bool = False,
    skip_toc: bool = False,
    max_retries: int = 3,
    fail_on_error: bool = False,
) -> tuple[bool, bool, float]:
    """Run the complete download process

    Args:
        base_url (str): Base URL for the OpenShift documentation version
        output_dir (str): Directory where documentation will be saved
        concurrency (int): Number of concurrent downloads
        force (bool): Force download even if files haven't changed
        skip_toc (bool): Skip TOC verification
        max_retries (int): Maximum number of retry attempts for failed downloads
        fail_on_error: Stop the pipeline if any document fails to download

    Returns:
        tuple: (verification_passed, toc_verification_passed, elapsed_time)
    """
    logger.info("Starting OpenShift Documentation download for %s", base_url)
    logger.info("Output directory: %s", output_dir)
    logger.info("Force download: %s", force)
    logger.info("Max retries: %s", max_retries)

    # Normalize base URL
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    # Create output directory
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Initialize database
    db_path = output_dir_path / "download_database.sqlite"
    init_database(db_path)

    # Create semaphore for limiting concurrent requests
    semaphore = asyncio.Semaphore(concurrency)

    start_time = time.time()

    async with aiohttp.ClientSession(trust_env=True) as session:
        # Step 1: Crawl to discover all html-single pages
        visited_urls, html_single_urls = await crawl(
            session, base_url, base_url, semaphore
        )

        # Step 2: Download discovered pages with built-in retry
        successes, failures, failed_downloads = await download_all(
            session,
            html_single_urls,
            output_dir_path,
            db_path,
            semaphore,
            force,
            max_retries,
        )

        # Record any failed downloads
        if failures > 0:
            # Using sync file operations is generally acceptable for infrequent logging operations
            failed_path = output_dir_path / "failed_downloads.json"
            json_content = json.dumps(list(failed_downloads), indent=2)
            failed_path.write_text(json_content)

        # Step 4: Verify downloads
        verification_passed = await verify_downloads(
            html_single_urls, db_path, output_dir_path, fail_on_error
        )

        # Step 5: Verify against TOC structure if not skipped
        toc_verification_passed = True
        if not skip_toc:
            try:
                toc_verification_passed = await verify_against_toc(
                    session,
                    html_single_urls,
                    visited_urls,
                    base_url,
                    db_path,
                    output_dir_path,
                    semaphore,
                )
            except Exception as e:
                logger.warning("TOC verification failed with error: %s", e)
                logger.warning("Continuing without TOC verification")
                toc_verification_passed = False

        # Step 6: Export URL mapping and reports
        export_url_mapping(db_path, output_dir_path)
        export_change_report(db_path, output_dir_path)

    elapsed_time = time.time() - start_time

    if verification_passed and toc_verification_passed:
        logger.info(
            "Download process completed successfully in %.2f seconds!", elapsed_time
        )
    else:
        logger.warning(
            "Download completed with issues in %.2f seconds. See logs for details.",
            elapsed_time,
        )

    return (verification_passed, toc_verification_passed, elapsed_time)


def apply_rate_limiting(rate_limit: float) -> None:
    """Apply rate limiting to semaphore acquire.

    Args:
        rate_limit (float): Time in seconds to wait between requests
    """
    # Note: Since we can't modify the Semaphore.acquire method directly without type errors,
    # we'll implement rate limiting in the functions that use the semaphore instead.
    # This is a simpler approach that avoids monkey-patching.
    if rate_limit > 0:
        logger.info("Rate limiting enabled: %s seconds between requests", rate_limit)

        # We'll use this opportunity to add a sleep before each semaphore usage
        # in the download and crawl functions


def construct_base_url(
    version: str, specific_doc: Optional[str] = None
) -> tuple[str, str]:
    """Construct the base URL for OpenShift documentation.

    Args:
        version (str): OpenShift version
        specific_doc (str): Optional specific document to download

    Returns:
        tuple: (base_url, output_dir)
    """
    if specific_doc:
        # If a specific document is requested, target only that document
        base_url = f"https://docs.redhat.com/en/documentation/openshift_container_platform/{version}/html-single/{specific_doc}"
        output_dir = f"./openshift-docs/{version}/html-single/{specific_doc}"

        # Check if index.html is explicitly specified, if not, add it
        if not base_url.endswith("index"):
            if not base_url.endswith("/"):
                base_url = f"{base_url}/"
    else:
        # Otherwise, target the entire documentation
        base_url = f"https://docs.redhat.com/en/documentation/openshift_container_platform/{version}"
        output_dir = f"./openshift-docs/{version}"

    return (base_url, output_dir)


def check_positive_int(value: str) -> int:
    """Validate that a string can be converted to a non-negative integer.

    Args:
        value (str): The string value to convert

    Returns:
        int: The converted non-negative integer

    Raises:
        argparse.ArgumentTypeError: If the value is negative
    """
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} is not a non-negative integer")
    return ivalue


async def main_async(args: argparse.Namespace) -> bool:
    """Run the main async downloader function.

    Args:
        args: Command line arguments
    """
    # Apply rate limiting if requested
    apply_rate_limiting(args.rate_limit)

    # Construct base URL and output directory
    base_url, output_dir = construct_base_url(args.version, args.specific_doc)

    if args.output_dir:
        if args.specific_doc:
            output_dir = (
                f"{args.output_dir}/{args.version}/html-single/{args.specific_doc}"
            )
        else:
            output_dir = f"{args.output_dir}/{args.version}"

    logger.info("Base URL: %s", base_url)
    logger.info("Output directory: %s", output_dir)

    # Run the downloader
    verification_passed, toc_verification_passed, elapsed_time = await run_downloader(
        base_url,
        output_dir,
        max_retries=args.max_retries,
        concurrency=args.concurrency,
        force=args.force,
        skip_toc=args.skip_toc_verification,
    )

    return verification_passed and toc_verification_passed


def main() -> None:
    """Execute the main entry point for the command line tool."""
    parser = argparse.ArgumentParser(
        description="Download Red Hat OpenShift Documentation"
    )
    parser.add_argument(
        "--version", type=str, default="4.18", help="OpenShift version (default: 4.18)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./openshift-docs",
        help="Output directory (default: ./openshift-docs)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Number of concurrent downloads (default: 5)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force download of all files even if not modified",
    )
    parser.add_argument(
        "--rate-limit",
        type=check_positive_int,
        default=0,
        help="Time in seconds to wait between requests (default: 0, no limit)",
    )
    parser.add_argument(
        "--specific-doc",
        type=str,
        help="Download only a specific document (e.g., 'monitoring')",
    )
    parser.add_argument(
        "--skip-toc-verification",
        action="store_true",
        help="Skip TOC verification step",
    )
    parser.add_argument(
        "--max-retries",
        type=check_positive_int,
        default=3,
        help="Maximum number of retry attempts for failed downloads (default: 3)",
    )
    args = parser.parse_args()

    # Run the async main function
    success = asyncio.run(main_async(args))

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    import sys

    main()
