# Module for loading and processing data
import pandas as pd

def load_excel_file(filepath):
    """Load an Excel file into a DataFrame."""
    return pd.read_excel(filepath)

def process_names(df):
    """Process the DataFrame to check name frequencies."""
    # Example processing, customize as needed
    name_counts = df['name'].value_counts()
    return name_counts
