import streamlit as st
import pandas as pd

from apps.main.upload.settings import *
from apps.widgets import dataframe as dtframe

def page_intro():
    st.markdown('## Merge Dataframes')
    with st.expander('More Info'):
        text = """
        **Currently, only left joins are supported.**

        *A left merge (left join) combines two tables based on a common key, including all rows from the left table and matching rows from the right table. 
        Unmatched rows from the right table have null values. 
        It preserves all rows from the left table while combining information from both tables.*

        1. Select the dataframe on the left.
        2. Select the columns you want to keep in the merged dataframe (you can discard irrelevant columns).
        3. Select the column(s) you want to merge on.
        4. Repeat steps 1-3 for the dataframe on the right.
        5. Click on the merge button.

        *Make sure the selected right column(s) to merge on is a primary key, i.e.: it contains unique values, to avoid duplicating recods on the left dataframe.*
        """
        st.markdown(text)

def select_dataframe():
    # Set global variables
    global left_df, right_df
    global left_col_selection, right_col_selection
    global left_index, right_index
    # Select left dataframe
    file_name, left_df = dtframe.select_dataframe('Select Left Dataframe')
    st.markdown('#### Left Columns to Keep:')
    left_col_selection = dtframe.select_dataframe_columns(
                                            left_df,
                                            label='Select columns to keep in the merged dataframe:', 
                                            key='left')
    st.markdown('#### Left Column(s) to Merge On:')
    left_index = dtframe.select_dataframe_columns(
                                            left_df,
                                            label='Select left column(s) to merge on:', 
                                            default='first', 
                                            key='left_index'
                                    )
    # Preview left dataframe
    dtframe.display_dataframe(left_df, file_name)
    st.markdown('---')

    # Select right dataframe
    file_name, right_df = dtframe.select_dataframe('Select Right Dataframe')
    st.markdown('#### Right Columns to Keep:')
    right_col_selection = dtframe.select_dataframe_columns(
                                            right_df,
                                            label='Select columns to keep in the merged dataframe:', 
                                            key='right')
    st.markdown('#### Right Column(s) to Merge On:')
    right_index = dtframe.select_dataframe_columns(
                                            right_df,
                                            label='Select right column(s) to merge on:', 
                                            default='first', 
                                            key='right_index'
                                    )
    # Preview right dataframe
    dtframe.display_dataframe(right_df, file_name)
    st.markdown('---')


def merge_dataframes():
    merge = st.button('Merge Dataframes', type='primary')
    if merge:
        with st.spinner('Merging dataframes...'):
            df = left_df[left_col_selection].merge(right_df[right_col_selection], how='left', left_on=left_index, right_on=right_index)
            st.session_state[DATAFRAME][MERGED] = df
        st.success('Dataframes merged and saved!')
        dtframe.display_dataframe(df, 'Merged Dataframe')

def merge_page():
    page_intro()

    if dtframe.are_there_dataframes():
        select_dataframe()
        merge_dataframes()
    else:
        dtframe.no_dataframe_yet()
