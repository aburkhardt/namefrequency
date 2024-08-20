import os
import pandas as pd
from datetime import datetime
from src.data_processing import load_excel_file
from src.name_scoring import load_national_datasets, load_local_frequencies, compare_against_datasets

def list_available_files(directory):
    """List all files in the given directory."""
    print(f"\nAvailable files in {directory}:")
    for filename in os.listdir(directory):
        print(f"- {filename}")

def check_file():
    directory = 'Check_file' 
    filename = input(f"Please enter the name of the Excel file you want to check (located in {directory}): ")
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        print(f"\nThe file '{filename}' does not exist in {directory}.")
        list_available_files(directory)  # List available files in the directory
        return
    
    df = load_excel_file(filepath)
    census_path = 'Data_Sources/census_last_names.csv'
    ssa_zip_path = 'Data_Sources/ssa_first_names.zip'
    processed_ssa_path = 'Data_Sources/processed_ssa_firstnames.csv'

    # Load the national datasets
    census_df, ssa_df = load_national_datasets(census_path, ssa_zip_path, processed_ssa_path)

    # Load local frequency data
    local_firstnames_df, local_lastnames_df = load_local_frequencies()

    # Compare the names in the Excel file against the national and local datasets
    df_scored = compare_against_datasets(df, census_df, ssa_df, local_firstnames_df, local_lastnames_df)

    # Determine output filename based on input file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'scored_{os.path.splitext(filename)[0]}_{timestamp}.xlsx'
    output_path = os.path.join('Check_file', output_filename)
    
    df_scored.to_excel(output_path, index=False)
    
    print(f'\nResults saved to {output_path}')

if __name__ == '__main__':
    check_file()
