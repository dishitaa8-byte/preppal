"""Helper functions for PrepPal application."""
import uuid
import os
from datetime import datetime


def generate_unique_id() -> str:
    """Generate a unique ID using UUID4."""
    return str(uuid.uuid4())


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename to prevent overwrites.
    
    Args:
        original_filename: Original filename from user upload
        
    Returns:
        Unique filename with timestamp and random UUID
    """
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = generate_unique_id()[:8]
    return f"{name}_{timestamp}_{unique_id}{ext.lower()}"


def get_upload_directory() -> str:
    """Get the absolute path to the uploads directory."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
