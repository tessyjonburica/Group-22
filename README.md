# CSV Data Cleaner and Validator (Group 22)

A Python CLI application that processes CSV files and detects & corrects data quality issues.

## Features

- Load and parse CSV files
- Detect data issues (missing values, type mismatches, format inconsistencies)
- Fix missing values using statistical methods
- Remove outliers using Z-score or IQR methods
- Normalize numeric data (min-max or z-score)
- Generate comprehensive reports

## Installation

1. Ensure Python 3.8+ is installed
2. No additional dependencies required (uses Python standard library only)

## Usage

```bash
python csv_data_cleaner.py
```

Follow the simple menu:
1. Load CSV file
2. Detect issues
3. Fix missing values
4. Remove outliers
5. Normalize data
6. Generate report
0. Exit

## Project Structure

```
Group 22/
├── csv_data_cleaner.py      # Main entry point
├── src/                     # Source code
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI interface
│   └── data_processors/    # Data processing modules
│       ├── __init__.py     # Package initialization
│       ├── base.py         # Abstract base classes
│       ├── csv_loader.py   # CSV file loading
│       ├── data_validator.py # Data validation
│       ├── missing_value_imputer.py # Missing value imputation
│       ├── outlier_remover.py # Outlier detection
│       ├── normalizer.py   # Data normalization
│       └── report_generator.py # Report generation
├── tests/                  # Unit tests
│   ├── __init__.py        # Package initialization
│   ├── test_csv_loader.py # Tests for CSV loader
│   └── test_data_validator.py # Tests for data validator
├── data/                   # Data files
│   └── sample_data.csv    # Sample input data
└── README.md              # This file
```

## Testing

Run individual tests:
```bash
python tests/test_csv_loader.py
python tests/test_data_validator.py
```

## Sample Data

The application includes `data/sample_data.csv` with various data quality issues for testing.
