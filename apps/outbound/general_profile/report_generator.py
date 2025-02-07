import streamlit as st
import pandas as pd
import numpy as np

from .settings import *
from . import utils as ut

def create_reports(dataframe: pd.DataFrame, selected_cols: dict):
    """The tables will have a datetime index grouped by monthly and daily, ORDER_ID, QTY and SKU_ID as columns.
    Therefore, each row of the table will report the total quantity and the number of orderlines per order. 

    The output will be something like this:

    **NEW OUTPUT HERE**

    Args:
        dataframe (pd.DataFrame): Dataframe to run the pivot table on
        selected_cols (dict): Group of column used by pivot table.
                              This parameter is created from the output of three st.selectbox in the following way:
                                  selected_cols = {
                                        QTY:qty_col,
                                        N_OLS: sku_col,
                                        N_ORDERS: order_col,
                                    }
    Return:
        dataframe (pd.DataFrame): Pivot table group by above criteria. E.g.:

    """
    business_pt = ut.pivot_on_datetime(dataframe, selected_cols, 'B')
    daily_pt = ut.pivot_on_datetime(dataframe, selected_cols, 'D')
    return business_pt, daily_pt


def dataset_report(dataframe: pd.DataFrame, selected_cols: dict,):
    st.markdown('### Dataset Reports')
    with st.expander('More Info'):
        text = """
        """
        st.markdown(text)

    # Genrate reports
    if st.button('Create Reports'):
        with st.spinner('Creating report...'):
            
            ut.overall_outbound_stats(dataframe, selected_cols)
            # Create first pivot table with order id as index
            try:
                business_report, daily_report = create_reports(dataframe, selected_cols)
                # Business Days Report
                b_percentile = ut.get_percentile(business_report, N_OLS)
                ut.save_df(b_percentile, BUSINESS_PERCENTILE)
                ut.add_dt_info(business_report)
                ut.save_df(business_report, BUSINESS_DAILY_REPORT)
                # Daily Report
                d_percentile = ut.get_percentile(daily_report, N_OLS)
                ut.save_df(d_percentile, DAILY_PERCENTILE)
                ut.add_dt_info(daily_report)
                ut.save_df(daily_report, DAILY_REPORT)
                st.success('Done!')

            except TypeError as e:
                error_message = f"""
                {str(e)}.

                **Please go to *Preprocess* section and set a proper datetime index.**
                """
                st.error(error_message)

    st.markdown('---')