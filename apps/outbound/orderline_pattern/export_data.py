import streamlit as st
import pandas as pd

from .settings import *
from . import utils as ut
from .report_dashboard import no_report_yet


@st.cache_data
def dataframe_to_csv(dataframe: pd.DataFrame):
    return dataframe.to_csv(sep='|', decimal=',', index=False).encode('utf-8')

def export_data_page():

    if not ut.get_df(FIRST_PT) is None:
        st.markdown('### Select Dataframe To Export')

        with st.spinner('Preparing data for dowmload...'):
            first_pt = ut.get_df(FIRST_PT)
            first_csv = dataframe_to_csv(first_pt)

            qty_report = ut.get_df(QTY_REPORT)
            qty_csv = dataframe_to_csv(qty_report)

            ol_report = ut.get_df(OL_REPORT)
            ol_csv = dataframe_to_csv(ol_report)

        st.info('Dataframe Preview')
        st.table(first_pt.head())
        st.download_button(
        label="Download Table",
        data=first_csv,
        file_name='first_pivot.csv',
        mime='text/csv',
        )
        st.markdown('---')

        st.info('Dataframe Preview')
        st.table(qty_report.reset_index().head())
        st.download_button(
        label="Download Table",
        data=qty_csv,
        file_name='quantity report.csv',
        mime='text/csv',
        )
        st.markdown('---')

        st.info('Dataframe Preview')
        st.table(ol_report.reset_index().head())
        st.download_button(
        label="Download Table",
        data=ol_csv,
        file_name='orderline report.csv',
        mime='text/csv',
        )
        st.markdown('---')

    else:
        no_report_yet()