import streamlit as st
import pandas as pd
import numpy as np

from .settings import *

def save_df(dataframe: pd.DataFrame, key: str):
    st.session_state[GENERAL_PROFILE][key] = dataframe

def get_df(key: str):
    return st.session_state[GENERAL_PROFILE].get(key)

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

def pivot_on_datetime(dataframe: pd.DataFrame, selected_cols: dict, freq: str):
    pt = dataframe.pivot_table(
                        index=[pd.Grouper(freq=freq), selected_cols[N_ORDERS]],
                        aggfunc={
                            selected_cols[QTY]:'sum', 
                            selected_cols[N_OLS]:'nunique'
                            }
                    )
    pt.reset_index(-1, inplace=True)

    pt = pt.pivot_table(
                        index=pd.Grouper(freq=freq),
                        aggfunc={
                            selected_cols[N_ORDERS]:'nunique',
                            selected_cols[QTY]:'sum', 
                            selected_cols[N_OLS]:'sum'
                            }
                    )

    # Rename pivot table columns to consistent naming
    rename_dict = renaming_dict(selected_cols)
    pt.rename(columns=rename_dict, inplace=True)

    # Convert quantity column to integer
    pt[QTY] = pt[QTY].astype(int)
    return pt

def add_dt_info(dataframe: pd.DataFrame):
    days = [dt.strftime('%A') for dt in dataframe.index]
    months = [dt.strftime('%b') for dt in dataframe.index]
    dataframe[DAYS] = days
    dataframe[MONTHS] = months    

def overall_outbound_stats(dataframe: pd.DataFrame, selected_cols: dict):
    stats = dict()
    # Total N orders
    stats[N_ORDERS] = dataframe[selected_cols[N_ORDERS]].nunique()
    # Total N Orderlines
    pt = dataframe.pivot_table( index=selected_cols[N_ORDERS],
                                aggfunc={selected_cols[N_OLS]:'nunique'})
    stats[N_OLS] = pt[selected_cols[N_OLS]].sum()
    # Total N SKUs
    stats[SKU_ID] = dataframe[selected_cols[N_OLS]].nunique()
    st.session_state[GENERAL_PROFILE][STATS] = stats

def get_percentile(dataframe: pd.DataFrame, column_name: str):
    a = dataframe[column_name].to_numpy()
    q = [i for i in range(0, 101, 1)]
    percentile =  np.nanpercentile(a, q)
    return pd.DataFrame(data=percentile, index=q, columns=[N_OLS])

@st.cache_data
def get_trend_line(array: np.array):
    X = [x for x in range(array.shape[0])]
    z = np.polyfit(X, array, 1)
    p = np.poly1d(z)
    return p(X)