"""
Normalizer Module for CSV Data Cleaner and Validator (Group 22)

This module contains the Normalizer class which performs normalization and standardization.
"""

import datetime
import statistics
from typing import List, Dict, Any
from .base import DataProcessor


class Normalizer(DataProcessor):
    """Performs normalization and standardization of numeric data."""
    
    def __init__(self, method: str = 'minmax'):
        """
        Initialize normalizer.
        
        Args:
            method: 'minmax' for min-max normalization or 'zscore' for standardization
        """
        self.method = method
        self.normalization_log = []
        self.scaling_params = {}
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize numeric columns.
        
        Args:
            data: List of dictionaries representing rows
            
        Returns:
            List of dictionaries with normalized values
        """
        if not data:
            return data
        
        headers = list(data[0].keys())
        cleaned_data = []
        
        # Identify numeric columns
        numeric_columns = []
        for header in headers:
            values = [row.get(header, '') for row in data]
            numeric_values = []
            for val in values:
                try:
                    if val and str(val).strip():
                        numeric_values.append(float(val))
                except ValueError:
                    pass
            
            if len(numeric_values) > len(values) * 0.5:  # More than 50% numeric
                numeric_columns.append(header)
        
        # Normalize each numeric column
        for column in numeric_columns:
            self._normalize_column(data, column)
        
        return data
    
    def _normalize_column(self, data: List[Dict[str, Any]], column: str) -> None:
        """Normalize a specific column."""
        values = []
        for i, row in enumerate(data):
            val = row.get(column, '')
            try:
                if val and str(val).strip():
                    values.append((float(val), i))
            except ValueError:
                pass
        
        if len(values) < 2:
            return
        
        numeric_values = [v[0] for v in values]
        
        if self.method == 'minmax':
            min_val = min(numeric_values)
            max_val = max(numeric_values)
            
            if max_val == min_val:
                return
            
            for val, row_idx in values:
                normalized_val = (val - min_val) / (max_val - min_val)
                data[row_idx][column] = normalized_val
                
                self.normalization_log.append({
                    'timestamp': datetime.datetime.now(),
                    'column': column,
                    'row': row_idx + 1,
                    'original_value': val,
                    'normalized_value': normalized_val,
                    'method': 'minmax',
                    'min': min_val,
                    'max': max_val
                })
            
            self.scaling_params[column] = {
                'method': 'minmax',
                'min': min_val,
                'max': max_val
            }
        
        else:  # zscore
            mean_val = statistics.mean(numeric_values)
            std_val = statistics.stdev(numeric_values)
            
            if std_val == 0:
                return
            
            for val, row_idx in values:
                z_score = (val - mean_val) / std_val
                data[row_idx][column] = z_score
                
                self.normalization_log.append({
                    'timestamp': datetime.datetime.now(),
                    'column': column,
                    'row': row_idx + 1,
                    'original_value': val,
                    'standardized_value': z_score,
                    'method': 'zscore',
                    'mean': mean_val,
                    'std': std_val
                })
            
            self.scaling_params[column] = {
                'method': 'zscore',
                'mean': mean_val,
                'std': std_val
            }
    
    def get_normalization_log(self) -> List[Dict[str, Any]]:
        """Return the normalization log."""
        return self.normalization_log 