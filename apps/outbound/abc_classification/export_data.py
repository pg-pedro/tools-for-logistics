import streamlit as st
import pandas as pd

from .settings import *
from . import utils as ut
from .report_dashboard import no_report_yet


@st.cache_data
def dataframe_to_csv(dataframe: pd.DataFrame):
    return dataframe.to_csv(sep='|', decimal=',').encode('utf-8')

def export_data_page():
    """
    Exports a dataframe as a csv and provides a download button for the file
    
    This function is used to export a dataframe as a csv file and display it on the front-end. It uses the function 'ut.get_df(FULL_REPORT)' to retrieve the dataframe to be exported.
    The function then converts the dataframe to csv using 'dataframe_to_csv(full_report)' and displays a preview of the dataframe.
    It also provides a download button for the file so that users can download the exported dataframe. If there is no dataframe yet, it calls another function 'no_report_yet()'
    
    Returns:
        None: This function does not return anything.
    """

    pick_report_exists = not ut.get_df(FULL_REPORT_ORDERLINES) is None
    qty_report_exists = not ut.get_df(FULL_REPORT_QTY) is None


    if pick_report_exists and qty_report_exists:
        st.markdown('### Select Dataframe To Export')

        with st.spinner('Preparing data for download...'):
            full_report = ut.get_df(FULL_REPORT_ORDERLINES)
            full_report_csv = dataframe_to_csv(full_report)


        st.info('Pick-line Report - Preview')
        st.table(full_report.reset_index().head())
        st.download_button(
        label="Download Table",
        data=full_report_csv,
        file_name='pickline report.csv',
        mime='text/csv',
        )
        st.markdown('---')

        with st.spinner('Preparing data for download...'):
            qty_report = ut.get_df(FULL_REPORT_QTY)
            qty_report_csv = dataframe_to_csv(qty_report)


        st.info('Quantity Report - Preview')
        st.table(qty_report.reset_index().head())
        st.download_button(
        label="Download Table",
        data=qty_report_csv,
        file_name='quantity report.csv',
        mime='text/csv',
        )
        st.markdown('---')

    else:
        no_report_yet()