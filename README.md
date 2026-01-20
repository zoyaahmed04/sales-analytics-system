# Sales Analytics System

## Overview
This project is a Python-based Sales Data Analytics System developed to clean,
validate, and analyze sales transaction data for an e-commerce company.

## Features
- Reads non-UTF-8 encoded sales data files
- Cleans messy data and removes invalid records
- Handles formatting issues such as commas in numbers and product names
- Validates business rules (quantity, price, IDs)
- Simulates API integration for product information
- Generates cleaned output files

## Project Structure
sales-analytics-system/
- main.py
- utils/
  - file_handler.py
  - data_processor.py
  - api_handler.py
- data/
  - sales_data.txt
- output/
  - cleaned_sales.txt
- requirements.txt

## How to Run
1. Install Python 3
2. Clone the repository
3. Run:
   python main.py

## Output
The system prints:
- Total records parsed
- Invalid records removed
- Valid records after cleaning

Cleaned sales data is saved in the output folder.
