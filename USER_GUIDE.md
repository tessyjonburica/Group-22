# CSV Data Cleaner - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Step-by-Step Workflow](#step-by-step-workflow)
4. [Understanding the Menu](#understanding-the-menu)
5. [Data Requirements](#data-requirements)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- CSV file with headers
- Basic understanding of data cleaning concepts

### Installation
1. Download the project files
2. Ensure Python is installed: `python --version`
3. No additional packages required (uses standard library only)

### Quick Start
```bash
python csv_data_cleaner.py
```

## Basic Usage

### First Time Users
1. **Load your data**: Choose option 1 and provide your CSV file path
2. **Check for issues**: Choose option 2 to see what problems exist
3. **Fix problems**: Use options 3-5 to clean your data
4. **Get results**: Choose option 6 to generate a report

### Example Session
```
=== CSV Data Cleaner (Group 22) ===

1. Load CSV file
2. Detect issues
3. Fix missing values
4. Remove outliers
5. Normalize data
6. Generate report
0. Exit

Choice (1-6): 1

--- Load CSV File ---
File path (or Enter for data/sample_data.csv): my_data.csv
✅ Loaded 150 rows

Choice (1-6): 2

--- Detect Issues ---
⚠️  Issues found:
   Non-numeric value 'abc' in numeric column 'Age' at row 45
   Invalid email format 'not-an-email' in email column 'Email' at row 67
   Missing value in Age column at row 23
```

## Step-by-Step Workflow

### Step 1: Load Your Data
- **What it does**: Reads your CSV file and validates its structure
- **What you need**: A CSV file with headers in the first row
- **Example input**: `my_data.csv` or press Enter for sample data
- **Success message**: "✅ Loaded X rows"

### Step 2: Detect Issues
- **What it does**: Analyzes your data for quality problems
- **Types of issues found**:
  - Missing values (empty cells)
  - Type mismatches (text in numeric columns)
  - Invalid formats (wrong email/date formats)
  - Data inconsistencies
- **What to expect**: List of specific problems with row numbers

### Step 3: Fix Missing Values
- **What it does**: Fills empty cells using statistical methods
- **Methods used**:
  - **Numeric columns**: Median (middle value)
  - **Text columns**: Mode (most frequent value)
- **What to expect**: "✅ Fixed X missing values"

### Step 4: Remove Outliers
- **What it does**: Identifies and removes extreme values
- **Methods available**:
  - **Z-score (default)**: Removes values beyond 2 standard deviations
  - **IQR**: Removes values outside 1.5 × interquartile range
- **What to expect**: "✅ Removed X outliers"

### Step 5: Normalize Data
- **What it does**: Scales numeric data to standard ranges
- **Methods available**:
  - **Min-max**: Scales to 0-1 range
  - **Z-score**: Centers around 0 with standard deviation 1
- **What to expect**: "✅ Normalized X values"

### Step 6: Generate Report
- **What it does**: Creates detailed summary of all changes
- **Report includes**:
  - Summary statistics
  - List of all transformations
  - Column type analysis
  - Recommendations
- **Save options**: Text report and cleaned CSV file

## Understanding the Menu

### Option 1: Load CSV File
- **Purpose**: Import your data for processing
- **Input**: File path (relative or absolute)
- **Default**: `data/sample_data.csv` if you press Enter
- **Requirements**: File must exist and be readable

### Option 2: Detect Issues
- **Purpose**: Find data quality problems
- **Prerequisite**: Must load data first (option 1)
- **Output**: List of specific issues with locations
- **Action**: Review issues before proceeding

### Option 3: Fix Missing Values
- **Purpose**: Fill empty cells automatically
- **Prerequisite**: Must load data first (option 1)
- **Methods**: Automatic selection based on data type
- **Safety**: Original data is preserved

### Option 4: Remove Outliers
- **Purpose**: Remove extreme values that skew analysis
- **Prerequisite**: Must load data first (option 1)
- **Choice**: Z-score (default) or IQR method
- **Impact**: Reduces dataset size

### Option 5: Normalize Data
- **Purpose**: Scale numeric data for analysis
- **Prerequisite**: Must load data first (option 1)
- **Choice**: Min-max (0-1) or Z-score (standardized)
- **Use case**: Machine learning, statistical analysis

### Option 6: Generate Report
- **Purpose**: Create comprehensive summary
- **Prerequisite**: Must load data first (option 1)
- **Output**: Detailed transformation log
- **Save options**: Report file and cleaned data

### Option 0: Exit
- **Purpose**: Safely close the application
- **Note**: Any unsaved changes will be lost

## Data Requirements

### CSV File Format
- **Headers**: Required in first row
- **Encoding**: UTF-8 recommended
- **Delimiter**: Comma (,) standard
- **Size**: No strict limit, but large files may be slow

### Supported Data Types
- **Numeric**: Integers, decimals, percentages
- **Text**: Names, descriptions, categories
- **Dates**: YYYY-MM-DD, MM/DD/YYYY, MM-DD-YYYY
- **Emails**: Standard email format validation

### Column Naming
- **Best practice**: Use descriptive names
- **Special columns**: 
  - Columns with "email" in name get email validation
  - Columns with "date" in name get date validation
- **Avoid**: Special characters in column names

## Output Files

### Report File (report.txt)
Contains detailed information about:
- Original vs cleaned data statistics
- All transformations performed
- Issues found and fixed
- Column type analysis
- Timestamps for all operations

### Cleaned Data File (cleaned.csv)
- Same structure as original file
- All transformations applied
- Missing values filled
- Outliers removed (if option 4 used)
- Numeric data normalized (if option 5 used)

## Troubleshooting

### Common Issues

#### "File not found" Error
- **Cause**: Incorrect file path
- **Solution**: Check file exists and path is correct
- **Tip**: Use relative paths or full absolute paths

#### "CSV file has no headers" Error
- **Cause**: First row doesn't contain column names
- **Solution**: Add headers to your CSV file
- **Example**: `Name,Age,Email,Salary`

#### "No data loaded" Error
- **Cause**: Trying to process data before loading
- **Solution**: Always use option 1 first
- **Workflow**: Load → Detect → Fix → Report

#### "No issues found" Message
- **Cause**: Your data is already clean
- **Action**: You can still normalize data (option 5)
- **Note**: This is good news!

#### "No outliers found" Message
- **Cause**: Your data doesn't have extreme values
- **Action**: Continue with normalization (option 5)
- **Note**: This is normal for clean datasets

### Performance Issues

#### Slow Processing
- **Cause**: Large file size
- **Solutions**:
  - Process smaller chunks
  - Close other applications
  - Use SSD storage if available

#### Memory Errors
- **Cause**: File too large for available memory
- **Solutions**:
  - Increase system RAM
  - Process smaller files
  - Use 64-bit Python

## Best Practices

### Before Processing
1. **Backup your data**: Always keep original files
2. **Review your data**: Understand what you're working with
3. **Check file size**: Large files may need special handling
4. **Validate format**: Ensure CSV is properly formatted

### During Processing
1. **Follow the workflow**: Load → Detect → Fix → Report
2. **Review issues**: Understand what problems exist
3. **Choose methods wisely**: Different methods for different data types
4. **Save results**: Don't lose your cleaned data

### After Processing
1. **Review the report**: Understand what changed
2. **Validate results**: Check that transformations make sense
3. **Backup cleaned data**: Save your processed files
4. **Document changes**: Keep notes on what was done

### Data Quality Tips
1. **Consistent formatting**: Use same date/email formats
2. **Meaningful headers**: Clear, descriptive column names
3. **Data types**: Ensure numeric columns contain numbers
4. **Missing values**: Decide how to handle empty cells

### File Management
1. **Organize files**: Use clear naming conventions
2. **Version control**: Keep track of different versions
3. **Backup strategy**: Regular backups of important data
4. **Storage**: Use reliable storage media

## Advanced Usage

### Batch Processing
For multiple files, you can:
1. Process each file individually
2. Save reports with descriptive names
3. Compare results across files
4. Create summary reports

### Custom Workflows
Common processing sequences:
- **Basic cleaning**: Load → Detect → Fix missing → Report
- **Statistical analysis**: Load → Detect → Fix missing → Remove outliers → Normalize → Report
- **Quality check**: Load → Detect → Report (no changes)

### Integration
The cleaned data can be used for:
- Statistical analysis
- Machine learning models
- Business intelligence
- Data visualization
- Further processing

## Support

### Getting Help
- Review this user guide
- Check the troubleshooting section
- Examine error messages carefully
- Test with sample data first

### Reporting Issues
When reporting problems, include:
- Error message text
- File size and format
- Steps to reproduce
- System information (Python version, OS)

### Feature Requests
For new features, consider:
- Use case description
- Expected behavior
- Sample data if applicable
- Priority level 