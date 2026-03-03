#!/usr/bin/env python3
"""
OSS Image Uploader for markdown-to-wechat skill.
Uploads local images to Aliyun OSS and returns public URLs.
"""

import os
import hashlib
from pathlib import Path
from typing import Optional


def get_oss_bucket(access_key_id: str, access_key_secret: str,
                   bucket_name: str, endpoint: str):
    """Create and return an OSS bucket instance."""
    try:
        import oss2
    except ImportError:
        raise ImportError(
            "oss2 package not found. Install with: pip install oss2"
        )
    auth = oss2.Auth(access_key_id, access_key_secret)
    return oss2.Bucket(auth, f"https://{endpoint}", bucket_name)


def get_file_hash(file_path: str) -> str:
    """Get MD5 hash of file for deduplication."""
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()[:8]


def upload_image(
    local_path: str,
    access_key_id: str,
    access_key_secret: str,
    bucket_name: str,
    endpoint: str,
    oss_dir: str = "wechat-articles",
) -> tuple:
    """
    Upload a local image to Aliyun OSS.

    Args:
        local_path: Path to the local image file
        access_key_id: Aliyun OSS Access Key ID
        access_key_secret: Aliyun OSS Access Key Secret
        bucket_name: OSS Bucket name
        endpoint: OSS endpoint (e.g. oss-cn-shanghai.aliyuncs.com)
        oss_dir: Directory prefix in OSS bucket

    Returns:
        (public_url, uploaded) where public_url is the OSS URL (or None on failure),
        and uploaded is True if the image was newly uploaded (False if skipped/cached).
    """
    local_path = Path(local_path)
    if not local_path.exists():
        print(f"  [WARNING] Image not found: {local_path}")
        return None, False

    try:
        bucket = get_oss_bucket(access_key_id, access_key_secret,
                                bucket_name, endpoint)

        # Build OSS key with hash suffix to avoid collisions
        file_hash = get_file_hash(str(local_path))
        stem = local_path.stem
        suffix = local_path.suffix
        oss_key = f"{oss_dir}/{stem}-{file_hash}{suffix}"

        # Check if already uploaded (idempotent)
        newly_uploaded = False
        try:
            import oss2
            bucket.head_object(oss_key)
            print(f"  [SKIP] Already uploaded: {oss_key}")
        except oss2.exceptions.NoSuchKey:
            # Upload the file
            bucket.put_object_from_file(oss_key, str(local_path))
            print(f"  [OK] Uploaded: {local_path.name} -> {oss_key}")
            newly_uploaded = True

        # Return the public URL and upload status
        return f"https://{bucket_name}.{endpoint}/{oss_key}", newly_uploaded

    except Exception as e:
        print(f"  [ERROR] Failed to upload {local_path.name}: {e}")
        return None, False


def upload_images_in_html(
    html_content: str,
    article_dir: str,
    access_key_id: str,
    access_key_secret: str,
    bucket_name: str,
    endpoint: str,
    oss_dir: str = "wechat-articles",
) -> tuple:
    """
    Find all local image references in HTML and upload them to OSS.
    Returns (html_with_updated_urls, upload_stats) where upload_stats is a dict
    with keys: total (local imgs found), uploaded (newly uploaded), skipped (cached).

    Args:
        html_content: HTML string with img src attributes
        article_dir: Directory where the source markdown file lives
        (used to resolve relative image paths)
        Other args: OSS connection details
    """
    import re

    article_dir = Path(article_dir)
    stats = {"total": 0, "uploaded": 0, "skipped": 0, "failed": 0}

    def replace_img(match):
        src = match.group(1)
        # Only process local paths (not http/https)
        if src.startswith("http://") or src.startswith("https://"):
            return match.group(0)

        stats["total"] += 1
        # Resolve relative path relative to article directory
        local_img_path = (article_dir / src).resolve()
        public_url, newly_uploaded = upload_image(
            str(local_img_path),
            access_key_id, access_key_secret,
            bucket_name, endpoint, oss_dir
        )

        if public_url:
            if newly_uploaded:
                stats["uploaded"] += 1
            else:
                stats["skipped"] += 1
            return match.group(0).replace(src, public_url)
        else:
            stats["failed"] += 1
            return match.group(0)

    # Match src="..." in img tags
    updated_html = re.sub(r'<img[^>]+src="([^"]+)"', replace_img, html_content)
    return updated_html, stats
