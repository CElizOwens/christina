import pandas as pd
import numpy as np

composers = pd.read_pickle('~/Python_Workspace/jupyter_workspace/opus_eda/composers.pkl')
works = pd.read_pickle('~/Python_Workspace/jupyter_workspace/opus_eda/works.pkl')

composers = composers.convert_dtypes()
works = works.convert_dtypes()

# set up works DataFrame
works_df = pd.DataFrame.from_records(works['intvals'])
works_df.drop(columns=['icatno', 'pageid'], inplace=True)
works_df['permlink'] = works.loc[:, 'permlink']

# set up composers DataFrame
composers_df = pd.DataFrame()
composers_df['id'] = composers.loc[:, 'id'].str[9:]
composers_df['permlink'] = composers.loc[:, 'permlink']
composers_df.rename(columns={'id': 'composer'}, inplace=True)

# this is a string array of works_df composers not found in composers_df
missing_composers = works_df.loc[~works_df['composer'].isin(composers_df['composer']), 'composer'].unique()
