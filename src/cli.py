"""
CLI Module for CSV Data Cleaner and Validator (Group 22)

This module contains the CLI class which manages user interaction and menu system.
"""

import csv
from .data_processors import (
    CSVLoader, DataValidator, MissingValueImputer, 
    OutlierRemover, Normalizer, ReportGenerator
)


class CLI:
    """Manages user interaction and menu system."""
    
    def __init__(self):
        self.csv_loader = CSVLoader()
        self.data_validator = DataValidator()
        self.imputer = MissingValueImputer()
        self.outlier_remover = OutlierRemover()
        self.normalizer = Normalizer()
        self.report_generator = ReportGenerator()
        self.current_data = []
        self.validation_results = {}
    
    def run(self):
        """Run the main CLI interface."""
        print("=== CSV Data Cleaner (Group 22) ===")
        
        while True:
            self._print_menu()
            choice = input("\nChoice (1-6): ").strip()
            
            if choice == '1':
                self._load_csv()
            elif choice == '2':
                self._detect_issues()
            elif choice == '3':
                self._impute_missing_values()
            elif choice == '4':
                self._remove_outliers()
            elif choice == '5':
                self._normalize_data()
            elif choice == '6':
                self._generate_report()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-6 or 0 to exit.")
    
    def _print_menu(self):
        """Print the simplified main menu."""
        print("\n1. Load CSV file")
        print("2. Detect issues")
        print("3. Fix missing values")
        print("4. Remove outliers")
        print("5. Normalize data")
        print("6. Generate report")
        print("0. Exit")
    
    def _load_csv(self):
        """Handle CSV file loading."""
        print("\n--- Load CSV File ---")
        
        file_path = input("File path (or Enter for data/sample_data.csv): ").strip()
        if not file_path:
            file_path = "data/sample_data.csv"
        
        if self.csv_loader.load_csv(file_path):
            self.current_data = self.csv_loader.get_data()
            print(f"✅ Loaded {len(self.current_data)} rows")
        else:
            print("❌ Failed to load file:")
            for issue in self.csv_loader.get_issues():
                print(f"   {issue}")
    
    def _detect_issues(self):
        """Handle data quality issue detection."""
        print("\n--- Detect Issues ---")
        
        if not self.current_data:
            print("❌ No data loaded. Use option 1 first.")
            return
        
        self.validation_results = self.data_validator.validate_data(
            self.current_data, self.csv_loader.get_headers()
        )
        
        if self.validation_results['valid']:
            print("✅ No issues found")
        else:
            print("⚠️  Issues found:")
            for issue in self.validation_results['issues']:
                print(f"   {issue}")
    
    def _impute_missing_values(self):
        """Handle missing value imputation."""
        print("\n--- Fix Missing Values ---")
        
        if not self.current_data:
            print("❌ No data loaded. Use option 1 first.")
            return
        
        self.current_data = self.imputer.process(self.current_data)
        log = self.imputer.get_imputation_log()
        
        if log:
            print(f"✅ Fixed {len(log)} missing values")
        else:
            print("✅ No missing values found")
    
    def _remove_outliers(self):
        """Handle outlier removal."""
        print("\n--- Remove Outliers ---")
        
        if not self.current_data:
            print("❌ No data loaded. Use option 1 first.")
            return
        
        method = input("Method (1=Z-score, 2=IQR): ").strip()
        if method == '2':
            self.outlier_remover = OutlierRemover(method='iqr')
        
        original_count = len(self.current_data)
        self.current_data = self.outlier_remover.process(self.current_data)
        removed = original_count - len(self.current_data)
        
        if removed > 0:
            print(f"✅ Removed {removed} outliers")
        else:
            print("✅ No outliers found")
    
    def _normalize_data(self):
        """Handle data normalization."""
        print("\n--- Normalize Data ---")
        
        if not self.current_data:
            print("❌ No data loaded. Use option 1 first.")
            return
        
        method = input("Method (1=Min-max, 2=Z-score): ").strip()
        if method == '2':
            self.normalizer = Normalizer(method='zscore')
        
        self.current_data = self.normalizer.process(self.current_data)
        log = self.normalizer.get_normalization_log()
        
        if log:
            print(f"✅ Normalized {len(log)} values")
        else:
            print("✅ No numeric data to normalize")
    
    def _generate_report(self):
        """Handle report generation."""
        print("\n--- Generate Report ---")
        
        if not self.current_data:
            print("❌ No data loaded. Use option 1 first.")
            return
        
        report = self.report_generator.generate_report(
            original_data=self.csv_loader.get_data(),
            cleaned_data=self.current_data,
            validation_results=self.validation_results,
            imputation_log=self.imputer.get_imputation_log(),
            outlier_log=self.outlier_remover.get_outlier_log(),
            normalization_log=self.normalizer.get_normalization_log()
        )
        
        print("📄 Report generated:")
        print(report)
        
        save = input("\nSave report? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Filename (default: report.txt): ").strip()
            if not filename:
                filename = "report.txt"
            
            if self.report_generator.save_report(report, filename):
                print(f"✅ Saved to {filename}")
            else:
                print("❌ Failed to save")
        
        save_csv = input("Save cleaned data? (y/n): ").strip().lower()
        if save_csv == 'y':
            filename = input("Filename (default: cleaned.csv): ").strip()
            if not filename:
                filename = "cleaned.csv"
            
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.csv_loader.get_headers())
                    writer.writeheader()
                    writer.writerows(self.current_data)
                print(f"✅ Saved to {filename}")
            except Exception as e:
                print(f"❌ Failed to save: {e}") 