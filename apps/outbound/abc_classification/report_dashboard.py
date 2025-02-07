import streamlit as st
import pandas as pd

from .settings import *
from . import utils as ut
from . import plot

def no_report_yet():
    text = """
    ### No Data To Show Yet!

    Please return to _Generate Report(s)_ section and make your selection.
    """
    st.markdown(text)


def overall_metrics():
    df = ut.get_df(FULL_REPORT_ORDERLINES)
    # Values to display
    global total_sku, total_orderlines, total_quantity
    total_sku = df.shape[0]
    total_orderlines = df[ORDERLINES].sum()
    total_quantity = df[QTY].sum()
    sku_per, pickline_per = ut.get_A_class(df)

    st.markdown('### Overall Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric('N SKUs', f'{total_sku:,}')
    col2.metric('Total Orderlines', f'{total_orderlines:,}')
    col3.metric(f'Total Qty', f'{total_quantity:,}')
    st.markdown('---')

def abc_sku_percentange_selector():
    st.markdown('### Select ABC Values')
    sku_percentage = st.slider(label='Select SKU %:', min_value=0, max_value=100, value=(20, 55))
    ut.abc_class_on_report(FULL_REPORT_ORDERLINES, sku_percentage)
    ut.abc_class_on_report(FULL_REPORT_QTY, sku_percentage)

def display_metrics(metrics_type: str):
    metrics = ut.get_abc_metrics(metrics_type)
    col1, col2, col3 = st.columns(3)
    # Column 1
    sku_abs = int(total_sku * (metrics.a_sku / 100))
    col1.metric(f'**A**: {metrics.a_sku} % - # {sku_abs:,}', f'{metrics.a_uom:,} %')
    # Column 2
    sku_abs = int(total_sku * (metrics.b_sku / 100))
    col2.metric(f'**B**: {metrics.b_sku} % - # {sku_abs:,}', f'{metrics.b_uom:,} %')
    # Column 3
    sku_abs = int(total_sku * (metrics.c_sku / 100))
    col3.metric(f'**C**: {metrics.c_sku} % - # {sku_abs:,}', f'{metrics.c_uom:,} %')


def dashboard_layout():
    """
    Generates a dashboard layout displaying the overall metrics and ABC classification plot.

    This function calls the 'overall_metrics' function to display overall metrics and the 'abc_line' function to display
    the ABC classification plot. The dataframe used is the 'FULL_REPORT' dataframe which should be loaded and saved before
    calling this function.
    """
    st.markdown('### Dashboard')
    # Overall metrics
    overall_metrics()
    # SKU Percentage Selector
    abc_sku_percentange_selector()
    # ABC Classification plot - Picklines
    st.markdown('### Orderlines')
    df = ut.get_df(FULL_REPORT_ORDERLINES)
    display_metrics(ORDERLINE_METRICS)
    fig = plot.abc_line(df, chart_type='ORDERLINES')
    st.plotly_chart(fig)
    st.markdown('---')
    # ABC Classification plot - Quantity
    st.markdown('### Quantity')
    df = ut.get_df(FULL_REPORT_QTY)
    display_metrics(QTY_METRICS)
    fig = plot.abc_line(df, chart_type='QTY')
    st.plotly_chart(fig)


def abc_pickline_dash():

    if not ut.get_df(FIRST_PIVOT) is None:
        dashboard_layout()
    else:
        no_report_yet()
