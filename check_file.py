import os
import pandas as pd
from src.data_processing import load_excel_file
from src.name_scoring import load_national_datasets, compare_against_national
from src.get_datasets import get_member_list, get_google_sheet_data

def list_available_files(directory):
    """List all files in the given directory."""
    print(f"\nAvailable files in {directory}:")
    for filename in os.listdir(directory):
        print(f"- {filename}")

def check_file():
    # Define the directory where files are stored
    directory = 'Check_file'  # Adjust this to the correct directory where your files are located
    
    # Ask the user for the file name
    filename = input(f"Please enter the name of the Excel file you want to check (located in {directory}): ")
    filepath = os.path.join(directory, filename)
    
    # Ensure the file exists
    if not os.path.exists(filepath):
        print(f"\nThe file '{filename}' does not exist in {directory}.")
        list_available_files(directory)  # List available files in the directory
        return

    # Define paths for the national datasets
    census_path = 'Data_Sources/census_last_names.csv'
    ssa_zip_path = 'Data_Sources/ssa_first_names.zip'

    # Load the Excel file
    df = load_excel_file(filepath)

    # Load the national datasets
    census_df, ssa_df = load_national_datasets(census_path, ssa_zip_path)

    # Fetch additional data sources
    member_list = get_member_list()
    google_sheet_data = get_google_sheet_data()

    # Compare the names in the Excel file against the national datasets
    df_scored = compare_against_national(df, census_df, ssa_df, member_list, google_sheet_data)

    # Determine output filename based on input file
    output_filename = os.path.join('Check_file', f'scored_{os.path.basename(filename)}')
    df_scored.to_excel(output_filename, index=False)
    
    print(f'\nResults saved to {output_filename}')

if __name__ == '__main__':
    check_file()
