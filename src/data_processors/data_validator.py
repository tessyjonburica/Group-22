"""
Data Validator Module for CSV Data Cleaner and Validator (Group 22)

This module contains the DataValidator class which validates data types and formats.
"""

import re
from typing import List, Dict, Any


class DataValidator:
    """Validates data types and formats."""
    
    def __init__(self):
        self.validation_issues = []
        self.column_types = {}
    
    def validate_data(self, data: List[Dict[str, Any]], headers: List[str]) -> Dict[str, Any]:
        """
        Validate data types and formats for each column.
        
        Args:
            data: List of dictionaries representing rows
            headers: List of column headers
            
        Returns:
            Dict containing validation results
        """
        self.validation_issues = []
        self.column_types = {}
        
        if not data or not headers:
            self.validation_issues.append("No data or headers to validate")
            return {"valid": False, "issues": self.validation_issues}
        
        # Analyze each column
        for header in headers:
            column_data = [row.get(header, '') for row in data]
            self._analyze_column(header, column_data)
        
        return {
            "valid": len(self.validation_issues) == 0,
            "issues": self.validation_issues,
            "column_types": self.column_types
        }
    
    def _analyze_column(self, header: str, column_data: List[Any]) -> None:
        """Analyze a single column for type and format issues."""
        # Remove empty values for analysis
        non_empty_data = [str(val).strip() for val in column_data if val and str(val).strip()]
        
        if not non_empty_data:
            self.column_types[header] = "unknown"
            return
        
        # Check for numeric data
        numeric_count = 0
        for val in non_empty_data:
            try:
                float(val)
                numeric_count += 1
            except ValueError:
                pass
        
        numeric_ratio = numeric_count / len(non_empty_data)
        
        if numeric_ratio > 0.8:
            self.column_types[header] = "numeric"
            # Check for type inconsistencies
            for i, val in enumerate(column_data):
                if val and str(val).strip():
                    try:
                        float(val)
                    except ValueError:
                        self.validation_issues.append(
                            f"Non-numeric value '{val}' in numeric column '{header}' at row {i+1}"
                        )
        else:
            # Check for date format
            date_count = 0
            for val in non_empty_data:
                if self._is_valid_date(val):
                    date_count += 1
            
            date_ratio = date_count / len(non_empty_data)
            
            if date_ratio > 0.8:
                self.column_types[header] = "datetime"
                # Check for date format inconsistencies
                for i, val in enumerate(column_data):
                    if val and str(val).strip() and not self._is_valid_date(val):
                        self.validation_issues.append(
                            f"Invalid date format '{val}' in date column '{header}' at row {i+1}"
                        )
            else:
                self.column_types[header] = "categorical"
                
                # Check for email format if column name suggests it
                if 'email' in header.lower():
                    for i, val in enumerate(column_data):
                        if val and str(val).strip() and not self._is_valid_email(val):
                            self.validation_issues.append(
                                f"Invalid email format '{val}' in email column '{header}' at row {i+1}"
                            )
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Check if string is a valid date format."""
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, date_str):
                return True
        return False
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if string is a valid email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email)) 