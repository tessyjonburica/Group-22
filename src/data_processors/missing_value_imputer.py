"""
Missing Value Imputer Module for CSV Data Cleaner and Validator (Group 22)

This module contains the MissingValueImputer class which handles imputation of missing values.
"""

import datetime
import statistics
import collections
from typing import List, Dict, Any
from .base import DataProcessor


class MissingValueImputer(DataProcessor):
    """Handles imputation of missing values using statistical methods."""
    
    def __init__(self):
        self.imputation_log = []
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Impute missing values using appropriate statistical methods.
        
        Args:
            data: List of dictionaries representing rows
            
        Returns:
            List of dictionaries with imputed values
        """
        if not data:
            return data
        
        headers = list(data[0].keys())
        cleaned_data = []
        
        for row in data:
            cleaned_row = row.copy()
            
            for header in headers:
                value = row.get(header, '')
                
                # Check if value is missing or empty
                if not value or str(value).strip() == '':
                    imputed_value = self._impute_value(header, data)
                    cleaned_row[header] = imputed_value
                    
                    self.imputation_log.append({
                        'timestamp': datetime.datetime.now(),
                        'column': header,
                        'row': len(cleaned_data) + 1,
                        'original_value': value,
                        'imputed_value': imputed_value,
                        'method': self._get_imputation_method(header, data)
                    })
            
            cleaned_data.append(cleaned_row)
        
        return cleaned_data
    
    def _impute_value(self, column: str, data: List[Dict[str, Any]]) -> Any:
        """Determine appropriate imputation method and return imputed value."""
        # Extract non-empty values for the column
        values = [row.get(column, '') for row in data]
        non_empty_values = [v for v in values if v and str(v).strip()]
        
        if not non_empty_values:
            return ''
        
        # Try to determine if numeric
        numeric_values = []
        for val in non_empty_values:
            try:
                numeric_values.append(float(val))
            except ValueError:
                pass
        
        if numeric_values:
            # Use median for numeric data (more robust than mean)
            return statistics.median(numeric_values)
        else:
            # Use mode for categorical data
            value_counts = collections.Counter(non_empty_values)
            return value_counts.most_common(1)[0][0]
    
    def _get_imputation_method(self, column: str, data: List[Dict[str, Any]]) -> str:
        """Get the imputation method used for a column."""
        values = [row.get(column, '') for row in data]
        non_empty_values = [v for v in values if v and str(v).strip()]
        
        if not non_empty_values:
            return 'no_data'
        
        numeric_values = []
        for val in non_empty_values:
            try:
                numeric_values.append(float(val))
            except ValueError:
                pass
        
        if numeric_values:
            return 'median'
        else:
            return 'mode'
    
    def get_imputation_log(self) -> List[Dict[str, Any]]:
        """Return the imputation log."""
        return self.imputation_log 