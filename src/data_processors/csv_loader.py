"""
CSV Loader Module for CSV Data Cleaner and Validator (Group 22)

This module contains the CSVLoader class which handles loading and basic validation of CSV files.
"""

import csv
import os
from typing import List, Dict, Any


class CSVLoader:
    """Handles loading and basic validation of CSV files."""
    
    def __init__(self):
        self.data = []
        self.headers = []
        self.file_path = ""
        self.issues = []
    
    def load_csv(self, file_path: str) -> bool:
        """
        Load CSV file and perform basic validation.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                self.issues.append(f"File not found: {file_path}")
                return False
            
            if not file_path.lower().endswith('.csv'):
                self.issues.append("File must have .csv extension")
                return False
            
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.headers = reader.fieldnames
                
                if not self.headers:
                    self.issues.append("CSV file has no headers")
                    return False
                
                self.data = list(reader)
                self.file_path = file_path
                
                if not self.data:
                    self.issues.append("CSV file is empty")
                    return False
                
                return True
                
        except Exception as e:
            self.issues.append(f"Error reading CSV file: {str(e)}")
            return False
    
    def get_data(self) -> List[Dict[str, Any]]:
        """Return the loaded data."""
        return self.data
    
    def get_headers(self) -> List[str]:
        """Return the column headers."""
        return self.headers
    
    def get_issues(self) -> List[str]:
        """Return any loading issues."""
        return self.issues 