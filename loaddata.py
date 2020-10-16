#!/usr/bin/env python3

import pandas as pd
import numpy as np
from website.config import testDatabaseURI
from sqlalchemy import create_engine, text


engine = create_engine(testDatabaseURI, echo=False)

composers = pd.read_pickle('~/Python_Workspace/jupyter_workspace/opus_eda/composers.pkl')
works = pd.read_pickle('~/Python_Workspace/jupyter_workspace/opus_eda/works.pkl')

composers = composers.convert_dtypes()
works = works.convert_dtypes()

# set up works DataFrame
works_df = pd.DataFrame.from_records(works['intvals'])
works_df.drop(columns=['icatno', 'pageid'], inplace=True)
works_df['link'] = works.loc[:, 'permlink']
works_df.rename(columns={'composer': 'name', 'worktitle': 'title'}, inplace=True)
works_df = works_df.convert_dtypes()
print(f"\nworks_df:\n")
works_df.info()

# set up composers DataFrame
composers_df = pd.DataFrame()
composers_df['name'] = composers.loc[:, 'id'].str[9:]
composers_df['link'] = composers.loc[:, 'permlink']
print(f"\ncomposers_df:\n")
composers_df.info()
# this is a DataFrame of works_df composers not found in composers_df
missing = pd.DataFrame(works_df.loc[~works_df['name'].isin(composers_df['name']), 'name'].unique(), columns=['name'])

# concatenate composers_df and missing; sort by composer; reset index
composers_df = pd.concat([composers_df, missing], ignore_index=True).sort_values('name').reset_index(drop=True)


# helper method: given composer_name, return id
def get_composer_id(name, connection):
    result = connection.execute(text("SELECT c.id FROM composer c WHERE c.name = :name;"), name=name)
    row = result.fetchone()
    return row['id']


# populate mysql composer and piece tables
# composer table first because piece table uses composer_id
with engine.begin() as con:
    print("Loading composer data into table...\n")
    for idx in range(len(composers_df)):
        name = composers_df.iloc[idx]['name']
        link = composers_df.iloc[idx]['link']
        con.execute(text("INSERT INTO composer (name, link) VALUES (:name, :link);"), name=name, link=link)

    # composers_df.to_sql('composer', con=con, if_exists='append')

    # REDO SECOND HALF OF THIS!!!
    print("Composer table loaded.\n")

# UNCOMMENT FROM HERE...

    print("Loading piece table...\n")
    for row in works_df.index:
        composer_id = get_composer_id(works_df.loc[row, 'name'], con)
        title = works_df.loc[row, 'title']
        link = works_df.loc[row, 'link']
        con.execute(text("INSERT INTO piece (composer_id, title, link) VALUES (:composer_id, :title, :link);"), composer_id=composer_id, title=title, link=link)

    # works_df.to_sql('piece', con=con, if_exists='append')

print("Piece table loaded. Done.\n")

# ...TO HERE.




# for row in works_df:
# INSERT row INTO piece given title, link, get_composer_id(composer_name)
