"""
Tests for data validation functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from PIL import Image
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.validate_data import validate_image_files, validate_captions_file


class TestDataValidation:
    """Test cases for data validation functions."""
    
    def test_validate_image_files_empty_directory(self):
        """Test validation with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_image_files(temp_dir)
            assert result is True
    
    def test_validate_image_files_nonexistent_directory(self):
        """Test validation with non-existent directory."""
        result = validate_image_files("nonexistent_directory")
        assert result is False
    
    def test_validate_image_files_with_valid_images(self):
        """Test validation with valid images."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a valid test image
            test_image = Image.new('RGB', (100, 100), color='red')
            test_image_path = os.path.join(temp_dir, 'test.jpg')
            test_image.save(test_image_path)
            
            result = validate_image_files(temp_dir)
            assert result is True
    
    def test_validate_captions_file_nonexistent(self):
        """Test validation with non-existent captions file."""
        result = validate_captions_file("nonexistent_file.txt")
        assert result is False
    
    def test_validate_captions_file_valid_format(self):
        """Test validation with valid captions format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            # Write valid captions
            f.write("image1.jpg#0 A person is walking in the park\n")
            f.write("image1.jpg#1 Someone walking through a green area\n")
            f.write("image2.jpg#0 A dog is playing in the yard\n")
            f.write("image2.jpg#1 A pet dog running around\n")
            temp_file = f.name
        
        try:
            result = validate_captions_file(temp_file)
            assert result is True
        finally:
            os.unlink(temp_file)
    
    def test_validate_captions_file_invalid_format(self):
        """Test validation with invalid captions format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            # Write invalid captions
            f.write("invalid_line_without_hash\n")
            f.write("image1.jpg#invalid_number caption text\n")
            temp_file = f.name
        
        try:
            result = validate_captions_file(temp_file)
            assert result is False
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__])
