import pandas as pd
import zipfile

# Load SSA Baby Names data
local_path_ssa = 'Data_Sources\ssa_first_names.zip'
with zipfile.ZipFile(local_path_ssa, 'r') as z:
    dfs = []
    for file_name in z.namelist():
        if file_name.startswith("yob") and file_name.endswith(".txt"):
            with z.open(file_name) as file:
                df = pd.read_csv(file, names=['name', 'sex', 'number'])
                df['year'] = int(file_name[3:7])
                dfs.append(df)
df_ssa = pd.concat(dfs, ignore_index=True)
df_ssa = df_ssa[(df_ssa['year'] >= 1930) & (df_ssa['year'] <= 2010)]

# Group by name and calculate total frequency for first names
first_name_freq_national = df_ssa.groupby('name')['number'].sum().reset_index()
first_name_freq_national.columns = ['name', 'frequency']
first_name_freq_national['name'] = first_name_freq_national['name'].str.lower()

# Load U.S. Census surnames data
local_path_census = 'Data_Sources\census_last_names.csv'
df_census = pd.read_csv(local_path_census, usecols=['name', 'count'])
df_census.columns = ['name', 'frequency']
df_census['name'] = df_census['name'].str.lower()

# Now first_name_freq_national and last_name_freq_national hold the national datasets
