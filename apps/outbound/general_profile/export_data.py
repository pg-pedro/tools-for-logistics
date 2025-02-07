import streamlit as st
import pandas as pd

from .settings import *
from . import utils as ut
from .report_dashboard import no_report_yet


@st.cache_data
def dataframe_to_csv(dataframe: pd.DataFrame):
    return dataframe.to_csv(sep='|', decimal=',', index=False).encode('utf-8')

def export_data_page():

    if not ut.get_df(DAILY_REPORT) is None:
        st.markdown('### Select Dataframe To Export')

        with st.spinner('Preparing data for dowmload...'):
            daily_report = ut.get_df(DAILY_REPORT)
            daily_report_csv = dataframe_to_csv(daily_report)

            business_report = ut.get_df(BUSINESS_DAILY_REPORT)
            business_report_csv = dataframe_to_csv(business_report)


        st.info('Dataframe Preview - Daily')
        st.table(daily_report.reset_index().head())
        st.download_button(
        label="Download Daily Table",
        data=daily_report_csv,
        file_name='daily_report.csv',
        mime='text/csv',
        )

        st.info('Dataframe Preview - Business Days')
        st.table(business_report.reset_index().head())
        st.download_button(
        label="Download Business Days Table",
        data=business_report_csv,
        file_name='daily_report.csv',
        mime='text/csv',
        )

        st.markdown('---')

    else:
        no_report_yet()