#!/usr/bin/env python3

import pandas as pd
import numpy as np
from itertools import groupby
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
    print("\nLoading composer data into table...")

    # Filling composer table takes about 10 seconds
    comps_list = list(composers_df.itertuples(index=False, name=None))
    for name, link in comps_list:
        con.execute(text("INSERT IGNORE INTO composer (name, link) VALUES (:name, :link);"), name=name, link=link)

    # for idx in composers_df.index:
    #     row = composers_df.loc[idx]
    #     name = row['name']
    #     link = row['link']
    #     con.execute(text("INSERT INTO composer (name, link) VALUES (:name, :link);"), name=name, link=link)

    print("Composer table loaded.\n\nLoading piece table...")

    # Filling piece table takes a little less than 4 minutes
    works_list = list(works_df.itertuples(index=False, name=None))
    """
        params = {'title1': 'jijjiji', 'link1': 'ijiji', 'title2': ''}
        s = "INSERT INTO piece (composer_id, title, link)
        VALUES
        (:composer_id, :title1, :link1),
        (:composer_id, :title2, :link2),
        (:composer_id, :title3, :link3)"
    """

    # row[0] = name, row[1] = title, row[2] = link
    for name, group in groupby(works_list, lambda row: row[0]):
        composer_id = get_composer_id(name, con)
        for work in group:
            con.execute(text("INSERT IGNORE INTO piece (composer_id, title, link) VALUES (:composer_id, :title, :link);"), composer_id=composer_id, title=work[1], link=work[2])

print("Piece table loaded.\n\n'loaddata.py' FINISHED!\n")
