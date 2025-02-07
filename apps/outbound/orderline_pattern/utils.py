import streamlit as st
import pandas as pd

from .settings import *

def save_df(dataframe: pd.DataFrame, key: str):
    st.session_state.ol_pattern[key] = dataframe

def get_df(key: str):
    return st.session_state.ol_pattern.get(key)

def custom_range():
    return st.session_state[OL_PATTERN][OL_CUSTOM_RANGE]

# Helper functions
def append_to_colname(dataframe: pd.DataFrame, suffix: str):
    for col in dataframe.columns:
        dataframe.rename(columns={col:f'{col}{suffix}'}, inplace=True)

def compute_cumsum_dataframe(dataframe: pd.DataFrame, suffix='_CS'):
    df_cumsum = dataframe.cumsum()
    append_to_colname(df_cumsum, '_CS')
    return df_cumsum

def renaming_dict(selected_cols: dict):
    """Returns a dict used to rename selected columns
    that are relevant for the order pattern analysis.
    This ensures consistency throughout the orderline pattern app.

    Args:
        selected_cols (dict): Dictionary containing the relevant column as values.

    Returns:
        dict: Returns a flipped selected cols dict.
              To be used with pd.DataFrame.rename
    """
    d = dict()
    for k, v in selected_cols.items():
        d[v] = k
    return d

def groupby_params(groupby: str):
    params = dict()
    if groupby == 'quantity':
        params['index'] = QTY
        params['aggfunc'] = dict(N_ORDERS='nunique', N_OLS='sum')
    elif groupby == 'orderline':
        params['index'] = N_OLS
        params['aggfunc'] = dict(N_ORDERS='nunique', QTY='sum')
    else:
        raise Exception('Groupby keyword not supported')
    return params


