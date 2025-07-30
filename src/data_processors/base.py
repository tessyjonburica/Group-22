"""
Base classes for data processing operations.

This module contains the abstract base class that all data processors inherit from.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataProcessor(ABC):
    """Abstract base class for data processing operations."""
    
    @abstractmethod
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process the data and return the result.
        
        Args:
            data: List of dictionaries representing rows
            
        Returns:
            List of dictionaries with processed data
        """
        pass 