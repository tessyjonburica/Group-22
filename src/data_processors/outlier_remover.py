"""
Outlier Remover Module for CSV Data Cleaner and Validator (Group 22)

This module contains the OutlierRemover class which detects and removes outliers.
"""

import datetime
import statistics
from typing import List, Dict, Any, Tuple
from .base import DataProcessor


class OutlierRemover(DataProcessor):
    """Detects and removes outliers using statistical methods."""
    
    def __init__(self, method: str = 'zscore', threshold: float = 2.0):
        """
        Initialize outlier remover.
        
        Args:
            method: 'zscore' or 'iqr'
            threshold: Threshold for outlier detection
        """
        self.method = method
        self.threshold = threshold
        self.outlier_log = []
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove outliers from numeric columns.
        
        Args:
            data: List of dictionaries representing rows
            
        Returns:
            List of dictionaries with outliers removed
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
        
        # Remove outliers from each numeric column
        for column in numeric_columns:
            outliers = self._detect_outliers(data, column)
            self.outlier_log.extend(outliers)
        
        # Filter out rows with outliers
        outlier_rows = set()
        for outlier in self.outlier_log:
            outlier_rows.add(outlier['row'])
        
        cleaned_data = [row for i, row in enumerate(data) if i + 1 not in outlier_rows]
        
        return cleaned_data
    
    def _detect_outliers(self, data: List[Dict[str, Any]], column: str) -> List[Dict[str, Any]]:
        """Detect outliers in a specific column."""
        values = []
        for i, row in enumerate(data):
            val = row.get(column, '')
            try:
                if val and str(val).strip():
                    values.append((float(val), i + 1))
            except ValueError:
                pass
        
        if len(values) < 3:
            return []
        
        numeric_values = [v[0] for v in values]
        
        if self.method == 'zscore':
            return self._zscore_outliers(numeric_values, values, column)
        else:
            return self._iqr_outliers(numeric_values, values, column)
    
    def _zscore_outliers(self, numeric_values: List[float], values: List[Tuple[float, int]], column: str) -> List[Dict[str, Any]]:
        """Detect outliers using Z-score method."""
        mean_val = statistics.mean(numeric_values)
        std_val = statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0
        
        if std_val == 0:
            return []
        
        outliers = []
        for val, row_num in values:
            z_score = abs((val - mean_val) / std_val)
            if z_score > self.threshold:
                outliers.append({
                    'timestamp': datetime.datetime.now(),
                    'column': column,
                    'row': row_num,
                    'value': val,
                    'method': 'zscore',
                    'z_score': z_score
                })
        
        return outliers
    
    def _iqr_outliers(self, numeric_values: List[float], values: List[Tuple[float, int]], column: str) -> List[Dict[str, Any]]:
        """Detect outliers using IQR method."""
        sorted_values = sorted(numeric_values)
        q1 = sorted_values[len(sorted_values) // 4]
        q3 = sorted_values[3 * len(sorted_values) // 4]
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = []
        for val, row_num in values:
            if val < lower_bound or val > upper_bound:
                outliers.append({
                    'timestamp': datetime.datetime.now(),
                    'column': column,
                    'row': row_num,
                    'value': val,
                    'method': 'iqr',
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                })
        
        return outliers
    
    def get_outlier_log(self) -> List[Dict[str, Any]]:
        """Return the outlier detection log."""
        return self.outlier_log 