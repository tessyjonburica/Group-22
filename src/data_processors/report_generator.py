"""
Report Generator Module for CSV Data Cleaner and Validator (Group 22)

This module contains the ReportGenerator class which generates comprehensive data quality reports.
"""

import datetime
import collections
from typing import List, Dict, Any


class ReportGenerator:
    """Generates comprehensive data quality reports."""
    
    def __init__(self):
        self.report_log = []
    
    def generate_report(self, 
                       original_data: List[Dict[str, Any]],
                       cleaned_data: List[Dict[str, Any]],
                       validation_results: Dict[str, Any],
                       imputation_log: List[Dict[str, Any]],
                       outlier_log: List[Dict[str, Any]],
                       normalization_log: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive data quality report.
        
        Args:
            original_data: Original data before cleaning
            cleaned_data: Data after cleaning
            validation_results: Results from data validation
            imputation_log: Log of imputation operations
            outlier_log: Log of outlier removal operations
            normalization_log: Log of normalization operations
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("CSV DATA CLEANER AND VALIDATOR - QUALITY REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary statistics
        report.append("SUMMARY STATISTICS:")
        report.append("-" * 20)
        report.append(f"Original rows: {len(original_data)}")
        report.append(f"Cleaned rows: {len(cleaned_data)}")
        report.append(f"Rows removed: {len(original_data) - len(cleaned_data)}")
        report.append("")
        
        # Validation issues
        if validation_results.get('issues'):
            report.append("VALIDATION ISSUES:")
            report.append("-" * 20)
            for issue in validation_results['issues']:
                report.append(f"• {issue}")
            report.append("")
        
        # Column types
        if validation_results.get('column_types'):
            report.append("COLUMN TYPES:")
            report.append("-" * 20)
            for column, col_type in validation_results['column_types'].items():
                report.append(f"• {column}: {col_type}")
            report.append("")
        
        # Imputation summary
        if imputation_log:
            report.append("MISSING VALUE IMPUTATION:")
            report.append("-" * 30)
            imputation_summary = collections.defaultdict(int)
            for entry in imputation_log:
                method = entry.get('method', 'unknown')
                imputation_summary[method] += 1
            
            for method, count in imputation_summary.items():
                report.append(f"• {method.title()} imputation: {count} values")
            report.append("")
        
        # Outlier summary
        if outlier_log:
            report.append("OUTLIER DETECTION:")
            report.append("-" * 20)
            outlier_summary = collections.defaultdict(int)
            for entry in outlier_log:
                method = entry.get('method', 'unknown')
                outlier_summary[method] += 1
            
            for method, count in outlier_summary.items():
                report.append(f"• {method.upper()} method: {count} outliers detected")
            report.append("")
        
        # Normalization summary
        if normalization_log:
            report.append("NORMALIZATION/STANDARDIZATION:")
            report.append("-" * 30)
            norm_summary = collections.defaultdict(int)
            for entry in normalization_log:
                method = entry.get('method', 'unknown')
                norm_summary[method] += 1
            
            for method, count in norm_summary.items():
                report.append(f"• {method.upper()} method: {count} values processed")
            report.append("")
        
        # Detailed logs
        report.append("DETAILED TRANSFORMATION LOG:")
        report.append("-" * 30)
        
        all_operations = []
        all_operations.extend(imputation_log)
        all_operations.extend(outlier_log)
        all_operations.extend(normalization_log)
        
        # Sort by timestamp
        all_operations.sort(key=lambda x: x.get('timestamp', datetime.datetime.min))
        
        for operation in all_operations:
            timestamp = operation.get('timestamp', datetime.datetime.now())
            report.append(f"[{timestamp.strftime('%H:%M:%S')}] ")
            
            if 'imputed_value' in operation:
                report.append(f"Imputed '{operation['column']}' at row {operation['row']}: "
                           f"'{operation['original_value']}' → '{operation['imputed_value']}'")
            elif 'value' in operation and 'method' in operation:
                if operation['method'] == 'zscore':
                    report.append(f"Outlier detected in '{operation['column']}' at row {operation['row']}: "
                               f"value {operation['value']} (z-score: {operation['z_score']:.2f})")
                else:
                    report.append(f"Outlier detected in '{operation['column']}' at row {operation['row']}: "
                               f"value {operation['value']}")
            elif 'normalized_value' in operation:
                report.append(f"Normalized '{operation['column']}' at row {operation['row']}: "
                           f"{operation['original_value']:.2f} → {operation['normalized_value']:.4f}")
            elif 'standardized_value' in operation:
                report.append(f"Standardized '{operation['column']}' at row {operation['row']}: "
                           f"{operation['original_value']:.2f} → {operation['standardized_value']:.4f}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_report(self, report: str, output_path: str) -> bool:
        """
        Save the report to a file.
        
        Args:
            report: The report string to save
            output_path: Path where to save the report
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(report)
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False 