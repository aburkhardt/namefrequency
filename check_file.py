import os
import sys
import pandas as pd
from datetime import datetime
from src.data_processing import load_excel_file
from src.name_scoring import load_national_datasets, load_local_frequencies, compare_against_datasets

import os
import sys
import pandas as pd
from datetime import datetime
from src.data_processing import load_excel_file
from src.name_scoring import load_national_datasets, load_local_frequencies, compare_against_datasets

def check_file(filepath):
    # Ensure the file exists
    if not os.path.exists(filepath):
        print(f"\nThe file '{filepath}' does not exist.")
        return

    # Load the Excel file
    print("Loading the Excel file...")
    df = load_excel_file(filepath)

    # Prompt the user for the column headers to use
    print(f"Columns in the file: {', '.join(df.columns)}")
    first_name_col = input("Please enter the column header for first names: ")
    last_name_col = input("Please enter the column header for last names: ")

    # Check if __file__ is defined
    if '__file__' in globals():
        script_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        # Fallback to current working directory if __file__ is not defined
        script_dir = os.getcwd()
        
    project_root = os.path.dirname(script_dir)

    # Print paths for debugging
    print(f"script_dir: {script_dir}")
    print(f"project_root: {project_root}")

    # Load the national datasets
    print("Loading national datasets...")
    census_path = os.path.join(script_dir, 'Data_Sources', 'census_last_names.csv')
    ssa_zip_path = os.path.join(script_dir, 'Data_Sources', 'ssa_first_names.zip')
    processed_ssa_path = os.path.join(script_dir, 'Data_Sources', 'processed_ssa_firstnames.csv')

    # Print constructed paths for debugging
    print(f"census_path: {census_path}")
    print(f"ssa_zip_path: {ssa_zip_path}")
    print(f"processed_ssa_path: {processed_ssa_path}")

    census_df, ssa_df = load_national_datasets(census_path, ssa_zip_path, processed_ssa_path)
    
    # Load local frequency data
    print("Loading local frequency data...")
    local_firstnames_df, local_lastnames_df = load_local_frequencies()

    # Rename columns in df to match expected names
    df.rename(columns={first_name_col: 'first_name', last_name_col: 'last_name'}, inplace=True)

    # Compare the names in the Excel file against the national and local datasets
    print("Comparing first names and last names to datasets...")
    df_scored = compare_against_datasets(df, census_df, ssa_df, local_firstnames_df, local_lastnames_df)

    # Generate the output filename with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'scored_{os.path.splitext(os.path.basename(filepath))[0]}_{timestamp}.xlsx'
    output_dir = os.path.join(script_dir, 'Check_file')
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the scored data to an Excel file
    print("Saving the results...")
    df_scored.to_excel(output_path, index=False)
    
    print(f'\nResults saved to {output_path}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        check_file(filepath)
    else:
        print("No file provided. Please provide a file path as an argument.")
