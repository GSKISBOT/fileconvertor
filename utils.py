"""
Utility functions for file operations and helpers
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def cleanup_file(file_path: str):
    """Safely delete a file"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {e}")

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    if not filename:
        return ""
    return Path(filename).suffix.lower()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def is_supported_file_type(filename: str, supported_extensions: list) -> bool:
    """Check if file type is supported"""
    extension = get_file_extension(filename)
    return extension in supported_extensions

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def create_temp_directory(prefix: str = "telegram_bot_") -> str:
    """Create a temporary directory"""
    import tempfile
    return tempfile.mkdtemp(prefix=prefix)

def get_mime_type(filename: str) -> str:
    """Get MIME type based on file extension"""
    extension = get_file_extension(filename)
    mime_types = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.rtf': 'application/rtf',
        '.odt': 'application/vnd.oasis.opendocument.text',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff'
    }
    return mime_types.get(extension, 'application/octet-stream')

def validate_file_size(file_size: int, max_size: int = 20 * 1024 * 1024) -> bool:
    """Validate file size against maximum allowed size"""
    return file_size <= max_size

def extract_filename_without_extension(filename: str) -> str:
    """Extract filename without extension"""
    return Path(filename).stem

def ensure_directory_exists(directory_path: str):
    """Ensure directory exists, create if it doesn't"""
    os.makedirs(directory_path, exist_ok=True)
