"""PDF service for handling PDF uploads, validation, and text extraction."""
import os
import fitz  # PyMuPDF
from typing import Optional, Tuple
from utils.validators import validate_pdf_file
from utils.helpers import generate_unique_filename, get_upload_directory


class PDFService:
    """Service class for PDF-related operations."""
    
    def __init__(self, upload_dir: Optional[str] = None):
        """
        Initialize PDF service.
        
        Args:
            upload_dir: Directory to store uploaded files (uses default if not provided)
        """
        self.upload_dir = upload_dir or get_upload_directory()
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def save_pdf(self, file) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate and save a PDF file.
        
        Args:
            file: File object from Flask request
            
        Returns:
            Tuple of (success, filename, error_message)
        """
        # Validate file
        is_valid, error_message = validate_pdf_file(file)
        if not is_valid:
            return False, None, error_message
        
        # Generate unique filename
        original_filename = file.filename
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file
        try:
            file.save(file_path)
            return True, unique_filename, None
        except Exception as e:
            return False, None, f"Failed to save file: {str(e)}"
    
    def extract_text(self, filename: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Extract text from a PDF file.
        
        Args:
            filename: Name of the PDF file in upload directory
            
        Returns:
            Tuple of (success, extracted_text, error_message)
        """
        file_path = os.path.join(self.upload_dir, filename)
        
        if not os.path.exists(file_path):
            return False, None, "File not found"
        
        try:
            # Open PDF and extract text
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            return True, text, None
        except Exception as e:
            return False, None, f"Failed to extract text: {str(e)}"
    
    def delete_pdf(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Delete a PDF file from upload directory.
        
        Args:
            filename: Name of the PDF file to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        file_path = os.path.join(self.upload_dir, filename)
        
        if not os.path.exists(file_path):
            return False, "File not found"
        
        try:
            os.remove(file_path)
            return True, None
        except Exception as e:
            return False, f"Failed to delete file: {str(e)}"
