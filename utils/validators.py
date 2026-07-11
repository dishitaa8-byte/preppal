"""Validators for PrepPal application inputs."""
import os
from typing import Tuple, Optional


def validate_pdf_file(file, max_size_mb: int = 16) -> Tuple[bool, Optional[str]]:
    """
    Validate a PDF file.
    
    Args:
        file: File object from Flask request
        max_size_mb: Maximum allowed file size in megabytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file exists and has filename
    if not file or not file.filename:
        return False, "No file provided"
    
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        return False, "Only PDF files are allowed"
    
    # Check file size
    max_size_bytes = max_size_mb * 1024 * 1024
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > max_size_bytes:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    return True, None


def validate_topic(topic: str, min_length: int = 2, max_length: int = 500) -> Tuple[bool, Optional[str]]:
    """
    Validate a topic input.
    
    Args:
        topic: Topic string to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    topic = topic.strip()
    if not topic:
        return False, "Topic cannot be empty"
    
    if len(topic) < min_length:
        return False, f"Topic must be at least {min_length} characters"
    
    if len(topic) > max_length:
        return False, f"Topic cannot exceed {max_length} characters"
    
    return True, None
