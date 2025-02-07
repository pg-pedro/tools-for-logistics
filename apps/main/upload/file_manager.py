from random import random
from typing import NamedTuple

import streamlit as st
import pandas as pd

from .settings import *

def data_storage_initialize() -> None:
    """
    Initialize storage for uploaded data and dataframe in Streamlit session state. 
    This function creates the 'uploaded_data' and 'dataframe' keys in the session state 
    if they do not already exist, and assigns them empty dictionaries as their values. 
    This function should be called before using session state to store uploaded data or dataframes.
    Returns:
        - None
    """
    if UPLOADED not in st.session_state:
        # Save uploaded files to session state
        st.session_state[UPLOADED] = dict()

    if XL_FILE not in st.session_state:
        # Stores the excel files uploaded
        st.session_state[XL_FILE] = dict()

    if PROCESS_FILE not in st.session_state:
        # Stores the boolean parameter for processing the uploaded file
        st.session_state[PROCESS_FILE] = dict()

    if DATAFRAME not in st.session_state:
        st.session_state[DATAFRAME] = dict()

    if IMPORT_PARAMS not in st.session_state:
        st.session_state[IMPORT_PARAMS] = dict()

def session_uploaded_keys():
    return st.session_state[UPLOADED].keys()

def session_uploaded_items():
    return st.session_state[UPLOADED].items()

def session_dataframe_items():
    return st.session_state[DATAFRAME].items()

def session_dataframe_keys():
    return st.session_state[DATAFRAME].keys()

def get_uploaded_file(file_name: str):
    file = st.session_state[UPLOADED].get(file_name)
    return file

def get_dataframe(df_name: str):
    df = st.session_state[DATAFRAME].get(df_name)
    return df

def save_files_to_session_state(uploaded_files: list):
    """Save uploaded files to session state.

    Args:
        uploaded_files (list): Uploaded files.
    """
    for uploaded_file in uploaded_files:
        st.session_state[UPLOADED][uploaded_file.name] = uploaded_file


def save_dataframe_to_session_state(id:str, dataframe: pd.DataFrame):
    st.session_state[DATAFRAME][id] = dataframe

def are_there_uploaded_files():
    _return = False
    if st.session_state[UPLOADED]:
        _return = True
    return _return

def are_there_dataframes():
    _return = False
    if st.session_state[DATAFRAME]:
        _return = True
    return _return

def read_to_dataframe(file_name, filepath_or_buffer, **kwargs):
    func = select_read_function(file_name)
    return func(filepath_or_buffer, **kwargs)

def select_read_function(file_name):
    if file_name.lower().endswith('.xlsx'):
        return pd.read_excel
    elif file_name.lower().endswith('.csv'):
        return pd.read_csv

def select_dataframe(label = 'Please select dataframe to manipulate'):
    file_list = session_dataframe_keys()
    # Create selectbox widget
    selected_df = st.selectbox(label, options=file_list)
    return selected_df

def display_dataframe(
                dataframe: pd.DataFrame,
                file_name: str,
                container: NamedTuple, 
            ):
    # Display dataframe
    n_rows, n_cols = dataframe.shape
    text = f"""
    ##### {file_name} - Preview
    N. Rows: {n_rows} - N. Columns: {n_cols}
    """
    container.name.info(text)
    container.location.dataframe(dataframe.iloc[:N_ROWS])

def prepare_csv_file(file_name: str):
    st.markdown('##### Set Parameters:')
    # CSV Separator 
    sep = st.text_input(
        label='CSV Column Separator:',
        value=';',
        max_chars=3,
        placeholder='E.g.: |',
        key=f'{file_name}_sep',
    )
    # Decimal Point 
    _help = """
    Character to recognize as decimal point (e.g. use ‘,’ for European data)."""
    dec = st.text_input(
        label='Decimal Point:',
        value=',',
        max_chars=1,
        placeholder='E.g.: .',
        help=_help,
        key=f'{file_name}_dec',
    )
    params = {}
    params['sep'] = sep
    params['decimal'] = dec
    params['low_memory'] = False
    st.session_state[IMPORT_PARAMS][file_name] = params
    st.markdown('---')

def process_csv_file(file_name: str, _file):
    params = st.session_state[IMPORT_PARAMS].get(file_name)
    df = pd.read_csv(_file, **params)
    save_dataframe_to_session_state(file_name, df)
    return df

@st.cache_data
def dataframe_to_csv(dataframe: pd.DataFrame):
    return dataframe.to_csv(sep='|', decimal=',', index=False).encode('utf-8')

def prepare_excel_file(file_name: str):
    st.markdown('##### Set Parameters:')
    with st.spinner('Previewing Excel File...'):
        xl_file = get_uploaded_file(file_name)
        xl = pd.ExcelFile(xl_file)
    # Select Column(s) to import
    label = 'Please Select Sheet(s) To Import:'
    options = xl.sheet_names
    _help = f"""
    If you select more than one, all the columns will be stacked on top of each other.
    """
    selected_sheets = st.multiselect(
                            label=label, 
                            options=options,
                            default=options[0],
                            help=_help)
    params = {}
    params[SELECTED_SHEETS] = selected_sheets
    st.session_state[IMPORT_PARAMS][file_name] = params
    st.session_state[XL_FILE][file_name] = xl
    st.markdown('---')

def process_excel_file(file_name: str, _file):
    selected_sheets = st.session_state[IMPORT_PARAMS][file_name].get(SELECTED_SHEETS)
    params = st.session_state[IMPORT_PARAMS].get(file_name)
    # Parse loop
    df = pd.DataFrame()
    for i, sheet_name in enumerate(selected_sheets, 1):
        with st.spinner(f'Reading {sheet_name}'):
            tmp_df = _file.parse(sheet_name, **params)
            df = pd.concat([df, tmp_df], ignore_index=True)
    save_dataframe_to_session_state(file_name, df)
    return df