"""
Test cases for CSVLoader class.
"""

import unittest
import tempfile
import os
import csv
import sys
sys.path.append('src')

from src.data_processors.csv_loader import CSVLoader


class TestCSVLoader(unittest.TestCase):
    """Test cases for CSVLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.loader = CSVLoader()
        
        # Create a temporary CSV file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.temp_file.write("Name,Age,Email,Salary\n")
        self.temp_file.write("Alice,29,alice@email.com,54000\n")
        self.temp_file.write("Bob,32,bob@email.com,52000\n")
        self.temp_file.write("Charlie,28,charlie@email.com,48000\n")
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_csv_success(self):
        """Test successful CSV loading."""
        result = self.loader.load_csv(self.temp_file.name)
        
        self.assertTrue(result)
        self.assertEqual(len(self.loader.data), 3)
        self.assertEqual(self.loader.headers, ['Name', 'Age', 'Email', 'Salary'])
        self.assertEqual(self.loader.file_path, self.temp_file.name)
        self.assertEqual(len(self.loader.issues), 0)
    
    def test_load_csv_file_not_found(self):
        """Test loading non-existent file."""
        result = self.loader.load_csv("nonexistent.csv")
        
        self.assertFalse(result)
        self.assertIn("File not found", self.loader.issues[0])
    
    def test_load_csv_wrong_extension(self):
        """Test loading file with wrong extension."""
        temp_txt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_txt_file.write("Name,Age\nAlice,29\n")
        temp_txt_file.close()
        
        result = self.loader.load_csv(temp_txt_file.name)
        
        self.assertFalse(result)
        self.assertIn("File must have .csv extension", self.loader.issues[0])
        
        os.unlink(temp_txt_file.name)
    
    def test_get_data(self):
        """Test getting loaded data."""
        self.loader.load_csv(self.temp_file.name)
        data = self.loader.get_data()
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['Name'], 'Alice')
        self.assertEqual(data[0]['Age'], '29')
    
    def test_get_headers(self):
        """Test getting headers."""
        self.loader.load_csv(self.temp_file.name)
        headers = self.loader.get_headers()
        
        self.assertEqual(headers, ['Name', 'Age', 'Email', 'Salary'])


if __name__ == '__main__':
    unittest.main() 