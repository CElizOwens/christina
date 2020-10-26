#!/usr/bin/env python3

import pandas as pd
import numpy as np

""" Retrieve data from IMSLP """

# URL parameters, below, have been set specifically for this script
# alphabetized list of composers
composers_url = 'https://imslp.org/imslpscripts/API.ISCR.php?account=worklist/disclaimer=accepted/sort=id/type=1/retformat=json'
# list of works ordered by composer name
works_url = 'https://imslp.org/imslpscripts/API.ISCR.php?account=worklist/disclaimer=accepted/sort=parent/type=2/retformat=json'


# Data retrieval

# Remove extra columns ('metadata' row no longer exists)
extra_cols = ['start', 'limit', 'sortby', 'sortdirection', 'moreresultsavailable', 'timestamp', 'apiversion']


def remove_extra_cols(data):
    data.drop(columns=extra_cols, inplace=True)


# Retrieval function
def create_df(data_url):

    start = 0
    df = pd.DataFrame()
    more = True

    while more:
        url = f'{data_url}/start={start}'
        data = pd.read_json(url, orient='index')
        more = data.loc['metadata', 'moreresultsavailable']  # are there more records after this
        data.drop(index='metadata', inplace=True)  # metadata is unneeded in DataFrame

        end = start + len(data)
        # prepare indices of current chunk of data to continue from ending index in df
        data.set_index(pd.Index(np.arange(start, end)), inplace=True)
        df = pd.concat([df, data])
        start = end

    remove_extra_cols(df)  # remove cols related to 'metadata'

    return df.copy()


# Get composers
composers = create_df(composers_url)
composers.to_pickle("./composers.pkl")

# Get works
works = create_df(works_url)
works.to_pickle("./works.pkl")
