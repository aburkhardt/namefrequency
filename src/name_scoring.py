import pandas as pd

def load_national_datasets(census_path, ssa_zip_path, processed_ssa_path='Data_Sources/processed_ssa_firstnames.csv'):
    """Load and process national datasets for names."""
    
    census_df = pd.read_csv(census_path, usecols=['name', 'count'])
    census_df.columns = ['name', 'frequency']
    census_df['name'] = census_df['name'].str.lower()

    ssa_df = process_ssa_zip(ssa_zip_path, processed_ssa_path)
    
    return census_df, ssa_df

def process_ssa_zip(ssa_zip_path, processed_ssa_path='Data_Sources/processed_ssa_firstnames.csv'):
    """Process SSA baby names data from ZIP file, filter by years, and group by name."""
    import zipfile
    import os
    
    # Check if the processed file already exists
    if os.path.exists(processed_ssa_path):
        return pd.read_csv(processed_ssa_path)

    dfs = []
    
    with zipfile.ZipFile(ssa_zip_path, 'r') as z:
        for file_name in z.namelist():
            if file_name.startswith("yob") and file_name.endswith(".txt"):
                with z.open(file_name) as file:
                    df = pd.read_csv(file, names=['name', 'sex', 'number'])
                    df['year'] = int(file_name[3:7])
                    dfs.append(df)
    
    ssa_df = pd.concat(dfs, ignore_index=True)
    ssa_df_filtered = ssa_df[(ssa_df['year'] >= 1930) & (ssa_df['year'] <= 2010)]
    ssa_df_grouped = ssa_df_filtered.groupby('name')['number'].sum().reset_index()
    ssa_df_grouped.columns = ['name', 'frequency']
    ssa_df_grouped['name'] = ssa_df_grouped['name'].str.lower()
    
    # Save the processed data for future use
    ssa_df_grouped.to_csv(processed_ssa_path, index=False)
    
    return ssa_df_grouped

def load_local_frequencies():
    """Load local first and last name frequencies from CSV files."""
    firstnames_df = pd.read_csv('Data_Sources/hyperlocal_firstnames.csv')
    lastnames_df = pd.read_csv('Data_Sources/hyperlocal_lastnames.csv')
    return firstnames_df, lastnames_df

def calculate_name_score(name, dataset_df):
    """Calculate how common a name is in a given dataset."""
    name = name.lower()
    if name in dataset_df['name'].values:
        frequency = dataset_df.loc[dataset_df['name'] == name, 'frequency'].values[0]
        total_frequency = dataset_df['frequency'].sum()
        score = frequency / total_frequency
        return score
    else:
        return 0

def compare_against_datasets(df, census_df, ssa_df, local_firstnames_df, local_lastnames_df):
    """
    Compare names in a DataFrame against both national and local datasets,
    then add scoring and flagging with nuanced categories.

    Parameters:
    - df: DataFrame containing local data with first and last names.
    - census_df: DataFrame containing processed Census surname data.
    - ssa_df: DataFrame containing processed SSA baby names data.
    - local_firstnames_df: DataFrame containing local first name frequencies.
    - local_lastnames_df: DataFrame containing local last name frequencies.

    Returns:
    - df: Original DataFrame with added columns for scores and nuanced flags.
    """
    # Calculate individual scores for national data
    df['national_first_name_score'] = df['first_name'].apply(lambda x: calculate_name_score(x, ssa_df))
    df['national_last_name_score'] = df['last_name'].apply(lambda x: calculate_name_score(x, census_df))
    
    # Calculate scores for local data
    df['local_first_name_score'] = df['first_name'].apply(lambda x: calculate_name_score(x, local_firstnames_df))
    df['local_last_name_score'] = df['last_name'].apply(lambda x: calculate_name_score(x, local_lastnames_df))

    # Adjust the weighting: national vs local (local gets higher weight)
    df['combined_score'] = df['national_first_name_score'] + df['national_last_name_score'] + \
                           2 * df['local_first_name_score'] + 2 * df['local_last_name_score']

    # Determine thresholds for Red Flag and Yellow Flag
    red_threshold = df['combined_score'].quantile(0.90)
    yellow_threshold = df['combined_score'].quantile(0.80)
    
    # Apply nuanced flagging based on combined score
    df['flag'] = df['combined_score'].apply(lambda x: 'Red Flag' if x >= red_threshold else
                                                      'Yellow Flag' if x >= yellow_threshold else
                                                      'Low Concern')
    
    return df
