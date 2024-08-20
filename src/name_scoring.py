import pandas as pd
import zipfile

def load_national_datasets(census_path, ssa_path):
    """Load and process national datasets for names."""
    
    # Load Census surname data
    census_df = pd.read_csv(census_path, usecols=['name', 'count'])
    census_df.columns = ['name', 'frequency']
    census_df['name'] = census_df['name'].str.lower()

    # Load SSA baby names data
    #it's a zip file so more complicated
    ssa_df = process_ssa_zip(ssa_path)
    
    return census_df, ssa_df

def process_ssa_zip(ssa_path):
    """
    Process SSA baby names data from ZIP file, filter by years, and group by name.

    Parameters:
    - ssa_zip_path: Path to the ZIP file containing SSA baby names data.

    Returns:
    - df_ssa_grouped: DataFrame containing processed and grouped SSA baby names data.
    """
    dfs = []
    
    with zipfile.ZipFile(ssa_path, 'r') as z:
        for file_name in z.namelist():
            if file_name.startswith("yob") and file_name.endswith(".txt"):
                with z.open(file_name) as file:
                    df = pd.read_csv(file, names=['name', 'sex', 'number'])
                    df['year'] = int(file_name[3:7])
                    dfs.append(df)
    
    # Combine all yearly data into a single DataFrame
    df_ssa = pd.concat(dfs, ignore_index=True)

    # Filter by years 1930-2010
    df_ssa_filtered = df_ssa[(df_ssa['year'] >= 1930) & (df_ssa['year'] <= 2010)]

    # Group by name and calculate total frequency
    df_ssa_grouped = df_ssa_filtered.groupby('name')['number'].sum().reset_index()
    df_ssa_grouped.columns = ['name', 'frequency']
    df_ssa_grouped['name'] = df_ssa_grouped['name'].str.lower()

    return df_ssa_grouped

def calculate_name_score(name, national_df):
    """Calculate how common a name is in the national dataset."""
    name = name.lower()
    if name in national_df['name'].values:
        frequency = national_df.loc[national_df['name'] == name, 'frequency'].values[0]
        total_frequency = national_df['frequency'].sum()
        score = frequency / total_frequency
        return score
    else:
        return 0  # Return 0 if the name is not found

import pandas as pd

def compare_against_national(df, census_df, ssa_df, member_list, google_sheet_data):
    """
    Compare names in a DataFrame against national datasets, member list, and Google Sheet.

    Parameters:
    - df: DataFrame containing local data with first and last names.
    - census_df: DataFrame containing processed Census surname data.
    - ssa_df: DataFrame containing processed SSA baby names data.
    - member_list: DataFrame or list with current members' names.
    - google_sheet_data: DataFrame with names and frequencies from Google Sheets.

    Returns:
    - df: Original DataFrame with added columns for scores and flags.
    """
    # Calculate individual scores
    df['first_name_score'] = df['first_name'].apply(lambda x: calculate_name_score(x, ssa_df))
    df['last_name_score'] = df['last_name'].apply(lambda x: calculate_name_score(x, census_df))
    
    # Additional scoring based on member list and Google Sheet
    df['member_score'] = df['first_name'].apply(lambda x: calculate_name_score(x, member_list)) + \
                         df['last_name'].apply(lambda x: calculate_name_score(x, member_list))

    df['google_sheet_score'] = df['first_name'].apply(lambda x: calculate_name_score(x, google_sheet_data)) + \
                               df['last_name'].apply(lambda x: calculate_name_score(x, google_sheet_data))
    
    # Adjust the weighting
    df['combined_score'] = df['first_name_score'] + df['last_name_score'] + \
                           2 * df['member_score'] + 3 * df['google_sheet_score']

    # Determine the threshold for the top 20% most common names
    threshold = df['combined_score'].quantile(0.80)
    
    # Add a "Red Flag" column based on the combined score
    df['flag'] = df['combined_score'].apply(lambda x: 'Red Flag' if x >= threshold else 'Normal')
    
    return df