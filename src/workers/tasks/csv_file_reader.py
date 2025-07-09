from __future__ import annotations

import csv
import io
import logging
from typing import Dict, List, Optional, Tuple

import chardet
import pandas as pd

logger = logging.getLogger(__name__)


class CSVFileReader:
    """Helper class for reading and parsing CSV files from email attachments."""
    
    @staticmethod
    def detect_encoding(file_content: bytes) -> str:
        """
        Detect the encoding of a file.
        
        Args:
            file_content: Raw file content
            
        Returns:
            Detected encoding
        """
        try:
            detected = chardet.detect(file_content)
            encoding = detected.get('encoding', 'utf-8')
            if encoding:
                return encoding
        except Exception as e:
            logger.warning(f"Failed to detect encoding: {e}")
        
        return 'utf-8'
    
    @staticmethod
    def detect_delimiter(csv_content: str, sample_size: int = 1024) -> str:
        """
        Detect the CSV delimiter.
        
        Args:
            csv_content: CSV content as string
            sample_size: Number of characters to sample
            
        Returns:
            Detected delimiter
        """
        sample = csv_content[:sample_size]
        
        # Try common delimiters
        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {}
        
        for delimiter in delimiters:
            count = sample.count(delimiter)
            if count > 0:
                delimiter_counts[delimiter] = count
        
        if delimiter_counts:
            # Return the most common delimiter
            return max(delimiter_counts, key=delimiter_counts.get)
        
        return ','  # Default to comma
    
    @staticmethod
    def parse_csv_headers(file_content: bytes) -> Tuple[List[str], str, str]:
        """
        Parse CSV headers from file content.
        
        Args:
            file_content: Raw file content
            
        Returns:
            Tuple of (headers, encoding, delimiter)
        """
        try:
            # Detect encoding
            encoding = CSVFileReader.detect_encoding(file_content)
            
            # Decode content
            csv_content = file_content.decode(encoding, errors='replace')
            
            # Detect delimiter
            delimiter = CSVFileReader.detect_delimiter(csv_content)
            
            # Parse headers
            csv_reader = csv.reader(io.StringIO(csv_content), delimiter=delimiter)
            headers = next(csv_reader, [])
            
            # Clean headers
            cleaned_headers = []
            for header in headers:
                # Strip whitespace and replace problematic characters
                cleaned_header = str(header).strip().replace(' ', '_').replace('-', '_')
                cleaned_header = ''.join(c for c in cleaned_header if c.isalnum() or c == '_')
                if cleaned_header and not cleaned_header[0].isdigit():
                    cleaned_headers.append(cleaned_header.lower())
                else:
                    cleaned_headers.append(f'column_{len(cleaned_headers) + 1}')
            
            return cleaned_headers, encoding, delimiter
            
        except Exception as e:
            logger.error(f"Failed to parse CSV headers: {e}")
            return [], 'utf-8', ','
    
    @staticmethod
    def parse_csv_data(file_content: bytes, headers: List[str], encoding: str, delimiter: str) -> List[Dict[str, str]]:
        """
        Parse CSV data from file content.
        
        Args:
            file_content: Raw file content
            headers: Column headers
            encoding: File encoding
            delimiter: CSV delimiter
            
        Returns:
            List of row dictionaries
        """
        try:
            # Decode content
            csv_content = file_content.decode(encoding, errors='replace')
            
            # Parse data
            csv_reader = csv.reader(io.StringIO(csv_content), delimiter=delimiter)
            
            # Skip header row
            next(csv_reader, None)
            
            rows = []
            for row_data in csv_reader:
                # Create row dictionary
                row = {}
                for i, value in enumerate(row_data):
                    if i < len(headers):
                        row[headers[i]] = str(value).strip() if value else None
                    else:
                        row[f'extra_column_{i + 1}'] = str(value).strip() if value else None
                
                # Ensure all headers have values (even if None)
                for header in headers:
                    if header not in row:
                        row[header] = None
                
                rows.append(row)
            
            return rows
            
        except Exception as e:
            logger.error(f"Failed to parse CSV data: {e}")
            return []
    
    @staticmethod
    def validate_csv_content(file_content: bytes) -> Dict[str, any]:
        """
        Validate and analyze CSV content.
        
        Args:
            file_content: Raw file content
            
        Returns:
            Validation results
        """
        try:
            headers, encoding, delimiter = CSVFileReader.parse_csv_headers(file_content)
            
            if not headers:
                return {
                    'valid': False,
                    'error': 'No headers found',
                    'headers': [],
                    'encoding': encoding,
                    'delimiter': delimiter
                }
            
            # Parse a sample of data to validate structure
            sample_rows = CSVFileReader.parse_csv_data(file_content, headers, encoding, delimiter)
            
            return {
                'valid': True,
                'headers': headers,
                'encoding': encoding,
                'delimiter': delimiter,
                'row_count': len(sample_rows),
                'sample_rows': sample_rows[:5]  # First 5 rows for preview
            }
            
        except Exception as e:
            logger.error(f"CSV validation failed: {e}")
            return {
                'valid': False,
                'error': str(e),
                'headers': [],
                'encoding': 'utf-8',
                'delimiter': ','
            }