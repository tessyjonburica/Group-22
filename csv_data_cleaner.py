#!/usr/bin/env python3
"""
CSV Data Cleaner and Validator (Group 22)

A Python CLI application that processes CSV files and detects & corrects data quality issues.
Handles missing values, outliers, normalization, and generates reports.

Author: Group 22
"""

from src.cli import CLI


def main():
    """Main function to run the CLI application."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main() 