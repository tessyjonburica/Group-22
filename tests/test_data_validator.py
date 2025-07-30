"""
Test cases for DataValidator class.
"""

import unittest
import sys
sys.path.append('src')

from src.data_processors.data_validator import DataValidator


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = DataValidator()
        
        # Test data with various types and issues
        self.test_data = [
            {'Name': 'Alice', 'Age': '29', 'Email': 'alice@email.com', 'Salary': '54000'},
            {'Name': 'Bob', 'Age': '32', 'Email': 'bob@email.com', 'Salary': '52000'},
            {'Name': 'Charlie', 'Age': '28', 'Email': 'charlie@email.com', 'Salary': '48000'},
            {'Name': 'Diana', 'Age': 'abc', 'Email': 'diana@email.com', 'Salary': '60000'},  # Invalid age
            {'Name': 'Eve', 'Age': '30', 'Email': 'not-an-email', 'Salary': '55000'},  # Invalid email
            {'Name': 'Frank', 'Age': '35', 'Email': 'frank@email.com', 'Salary': '70000'}
        ]
        self.headers = ['Name', 'Age', 'Email', 'Salary']
    
    def test_validate_data_success(self):
        """Test successful data validation."""
        result = self.validator.validate_data(self.test_data, self.headers)
        
        self.assertIsInstance(result, dict)
        self.assertIn('valid', result)
        self.assertIn('issues', result)
        self.assertIn('column_types', result)
    
    def test_validate_data_empty_data(self):
        """Test validation with empty data."""
        result = self.validator.validate_data([], self.headers)
        
        self.assertFalse(result['valid'])
        self.assertIn("No data or headers to validate", result['issues'])
    
    def test_validate_data_numeric_column(self):
        """Test validation of numeric column."""
        numeric_data = [
            {'Age': '29', 'Salary': '54000'},
            {'Age': '32', 'Salary': '52000'},
            {'Age': '28', 'Salary': '48000'}
        ]
        headers = ['Age', 'Salary']
        
        result = self.validator.validate_data(numeric_data, headers)
        
        self.assertEqual(result['column_types']['Age'], 'numeric')
        self.assertEqual(result['column_types']['Salary'], 'numeric')
    
    def test_validate_data_categorical_column(self):
        """Test validation of categorical column."""
        categorical_data = [
            {'Name': 'Alice', 'Department': 'Engineering'},
            {'Name': 'Bob', 'Department': 'Marketing'},
            {'Name': 'Charlie', 'Department': 'Sales'}
        ]
        headers = ['Name', 'Department']
        
        result = self.validator.validate_data(categorical_data, headers)
        
        self.assertEqual(result['column_types']['Name'], 'categorical')
        self.assertEqual(result['column_types']['Department'], 'categorical')
    
    def test_is_valid_date(self):
        """Test date validation method."""
        valid_dates = ['2023-04-01', '04/01/2023', '04-01-2023']
        invalid_dates = ['2023/04/01', '01-04-2023', 'not-a-date']
        
        for date in valid_dates:
            self.assertTrue(self.validator._is_valid_date(date))
        
        for date in invalid_dates:
            self.assertFalse(self.validator._is_valid_date(date))
    
    def test_is_valid_email(self):
        """Test email validation method."""
        valid_emails = ['alice@email.com', 'bob@company.co.uk', 'test.user@domain.org']
        invalid_emails = ['not-an-email', 'alice@', '@email.com', 'alice.email.com']
        
        for email in valid_emails:
            self.assertTrue(self.validator._is_valid_email(email))
        
        for email in invalid_emails:
            self.assertFalse(self.validator._is_valid_email(email))


if __name__ == '__main__':
    unittest.main() 