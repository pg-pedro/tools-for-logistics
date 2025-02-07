from collections import namedtuple

import streamlit as st
import pandas as pd

from .settings import *

ABCMetrics = namedtuple('ABC_Metrics', 'a_sku a_uom b_sku b_uom c_sku c_uom')

def save_df(dataframe: pd.DataFrame, key: str):
    st.session_state[ABC_CLASS][key] = dataframe

def get_df(key: str):
    return st.session_state[ABC_CLASS].get(key)

def get_abc_metrics(key: str):
    return st.session_state[ABC_CLASS].get(key)

# Helper functions
def append_to_colname(dataframe: pd.DataFrame, suffix: str):
    for col in dataframe.columns:
        dataframe.rename(columns={col:f'{col}{suffix}'}, inplace=True)

def compute_cumsum_dataframe(dataframe: pd.DataFrame, suffix='_CS'):
    df_cumsum = dataframe.cumsum()
    append_to_colname(df_cumsum, '_CS')
    return df_cumsum

def renaming_dict(selected_cols: dict):
    """
    Returns a dictionary used to rename selected columns that are relevant 
    for the order pattern analysis. This ensures consistency throughout 
    the orderline pattern app.
    
    The selected columns which are passed in `selected_cols` argument 
    in the form of dictionary, this function will flip the keys and values of the passed
    dictionary, which can be used to rename columns in the pandas DataFrame.
    
    Args:
        selected_cols (dict): Dictionary containing relevant columns 
                              as values and the desired names of columns as keys.
                              
    Returns:
        dict: Returns a flipped selected_cols dictionary.
              To be used with pd.DataFrame.rename.
    """
    d = dict()
    for k, v in selected_cols.items():
        d[v] = k
    return d

def get_A_class(full_report: pd.DataFrame, chart_type: str = 'ORDERLINES'):
    """
    Returns the percentage of SKU and Picklines for class A
    
    This function creates a mask for the full_report dataframe, filtering only rows where the value of the SKU_PER column is greater than or equal to 20.
    It then selects the first row that matches this condition and extracts the values of the SKU_PER and ORDERLINES_PER columns, which correspond to the percentage of SKUs and picklines respectively.
    This is the A class, that represents around 20% of SKUs and 80% of Picklines.
    
    Args:
        full_report (pd.DataFrame): DataFrame containing the report, 
                                    the columns required are "SKU_PER" and "ORDERLINES_PER"
                                    
    Returns:
        float, float: Returns the values of SKU_PER and ORDERLINES_PER respectively, representing the percentage of class A
    """
    mask = full_report[SKU_PER] >= 20.0
    a_class_row = full_report[mask].iloc[0]
    # Get ~ 20 / 80 values 
    sku_per = a_class_row[SKU_PER]
    if chart_type == 'ORDERLINES':
        uom_per = a_class_row[ORDERLINES_PER]
    elif chart_type == 'QTY':
        uom_per = a_class_row[QTY_PER]
    return sku_per, uom_per

def groupby_params(groupby: str):
    """
    Returns a dictionary containing the parameters used to group a pandas DataFrame
    
    This function returns a dictionary with the index and aggregate function parameters that can be used to group a pandas DataFrame using the groupby method.
    The groupby parameter can take either "quantity" or "orderline" as values, depending on the column you want to group the data by.
    
    If the value is "quantity", the function will return a dictionary with "QTY" as the index and {"N_ORDERS": "nunique", "N_OLS": "sum"} as the aggregate function.
    If the value is "orderline", the function will return a dictionary with "N_OLS" as the index and {"N_ORDERS": "nunique", "QTY": "sum"} as the aggregate function.
    If another value is passed, an exception will be raised.
    
    Args:
        groupby (str): the column name to be used as the index of the returned dictionary
        
    Returns:
        dict: Returns a dictionary with the keys 'index' and 'aggfunc' 
              that can be used to group a pandas DataFrame using the groupby method.
              The value of 'index' will be the column name, and 'aggfunc' will be a dict
              of columns and their aggregate function.
    """
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

def get_abc_percentage_classes(sku_percentage: tuple):
    a_class = sku_percentage[0]
    b_class = sku_percentage[1] - a_class
    c_class = 100 - sku_percentage[1]
    return {'A': a_class, 'B': b_class, 'C': c_class}

def create_abc_metrics(dataframe: pd.DataFrame):
    ...

def abc_class_on_report(report_name: str, sku_percentage: tuple):
    # Conditions
    ORDERLINE_REPORT_requested = report_name == FULL_REPORT_ORDERLINES
    qty_report_requested = report_name == FULL_REPORT_QTY
    # Check if correct report name has been provided
    if ORDERLINE_REPORT_requested:
        df = get_df(report_name)
        report_col = ORDERLINES_PER
        report_metrics = ORDERLINE_METRICS
    elif qty_report_requested:
        df = get_df(report_name)
        report_col = QTY_PER
        report_metrics = QTY_METRICS
    else:
        error = f'Only {FULL_REPORT_ORDERLINES} or {FULL_REPORT_QTY} can be used.'
        raise KeyError(error)

    # Fill ABC Classification into selected report dataframe
    abc_class_dict = get_abc_percentage_classes(sku_percentage)
    df[ABC_COL] = 'C'
    B_CLASS = abc_class_dict['A'] + abc_class_dict['B']
    b_index = df[df[SKU_PER] <= B_CLASS].index
    df.loc[b_index, ABC_COL] = 'B'
    a_index = df[df[SKU_PER] <= abc_class_dict['A']].index
    df.loc[a_index, ABC_COL] = 'A'
    # Compute UoM usage per class
    a_uom = df.loc[a_index, report_col].iloc[-1]
    b_uom = df.loc[b_index, report_col].iloc[-1] - a_uom
    c_uom = 100 - (a_uom + b_uom)
    # Save current ABC Configuration
    abc_metrics = ABCMetrics(
                            abc_class_dict['A'], round(a_uom, 2), 
                            abc_class_dict['B'], round(b_uom, 2), 
                            abc_class_dict['C'], round(c_uom, 2)
                        )
    st.session_state[ABC_CLASS][report_metrics] = abc_metrics