import streamlit as st
import pandas as pd

from apps.main.upload.settings import *



def select_dataframe(custom_title: str = 'Select a dataframe:'):
    st.markdown(f'### {custom_title}')
    label = 'Please select dataframe:'
    options = st.session_state[DATAFRAME].keys()
    selected = st.selectbox(label, options, key=custom_title)
    df = st.session_state[DATAFRAME].get(selected)
    return selected, df

def select_dataframe_columns(
                    df: pd.DataFrame, 
                    label: str = 'Column Selection:',
                    default: str = 'all', 
                    key: str = '',
                    help: str = ''
                ):
    key = f'{key}_cols_selector'  # Set widget key
    cols = list(df.columns)

    # Default displayed values
    if default == 'all':
        _default = list(df.columns)
    elif default == 'first':
        _default = list(df.columns)[0]
    else:
        _default = list(df.columns)

    selection = st.multiselect(
                        label=label, 
                        options=cols,
                        default=_default, 
                        key=key,
                        help=help)
    return selection

def display_dataframe(
                dataframe: pd.DataFrame,
                file_name: str = 'Dataframe',
            ):
    """Display dataframe preview."""
    # Display dataframe
    n_rows, n_cols = dataframe.shape
    text = f"""
    ##### {file_name} - Preview
    N. Rows: {n_rows} - N. Columns: {n_cols}
    """
    st.info(text)
    st.dataframe(dataframe.iloc[:N_ROWS])

def is_index_datetime(df: pd.DataFrame):
    """Check if dataframe index is datetime."""
    return isinstance(df.index, pd.DatetimeIndex)

def datetime_index_warning(df: pd.DataFrame):
    """Check if dataframe index is datetime."""
    if not is_index_datetime(df):
        text = """
        ##### Warning!
        The dataframe index is not a datetime index.

        If you need to analyse the dataframe by time, please go to *Preprocess* section and set a proper datetime index.
        Otherwise you can ignore this warning.
        """
        st.warning(text)

def datetime_index_error(df: pd.DataFrame):
    """Check if dataframe index is datetime."""
    if not is_index_datetime(df):
        text = """
        #### Warning!
        The dataframe index is not a datetime index.

        **Please go to *Preprocess* section and set a proper datetime index.**

        """
        st.error(text)

def are_there_dataframes():
    _return = False
    if st.session_state[DATAFRAME]:
        _return = True
    return _return

def no_dataframe_yet():
    text = """
    #### No Dataframe yet!

    Please upload your data first.
    """
    st.markdown(text)