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

def outbound_stats():
    st.markdown('#### Outbound Stats')
    stats = st.session_state[GENERAL_PROFILE].get(STATS)
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(f'Total Orders', f'{stats[N_ORDERS]:,}')
    col2.metric('Total Orderlines', f'{stats[N_OLS]:,}')
    col3.metric('Total SKUs', f'{stats[SKU_ID]:,}')
    st.markdown('---')

def report_type_selector():
    st.markdown('#### Select Report Time Series Frequency')
    _help = """
This will group by the specified frequency.
It affects the output of the aggregation function. 

E.g.: Business days are Monday to Friday, therefore the computed percentile will be larger than calendar days (Mon - Sun).

Available selection:
- Business Report: Business day frequency (**Monday** to **Friday**)
- Daily Report   : Calendar day frequency (**Monday** to **Sunday**)

**This selection will be applied to the entire dashboard.**

    """
    label = """
    """
    report_type = st.selectbox(
        'Select Time Series Frequency:', 
        options=[DAILY_REPORT, BUSINESS_DAILY_REPORT], 
        format_func=lambda x: x.replace('_', ' ').title(),
        index=1,
        help=_help
    )
    st.markdown('---')
    return report_type

def get_report_type_context(report_type: str):
    if report_type == BUSINESS_DAILY_REPORT:
        title = 'Business Days'
        percentile_report = BUSINESS_PERCENTILE
    elif report_type == DAILY_REPORT:
        title = 'Daily'
        percentile_report = DAILY_PERCENTILE
    return title, percentile_report


def orderline_main_chart(report_type: str = BUSINESS_DAILY_REPORT):
    title, percentile_report = get_report_type_context(report_type)

    st.markdown(f'#### {title} Orderlines')
    # Percentile slider
    _help = f"""
Each of the 100 equal groups into which a population can be divided according to the distribution of values of a particular variable.
    """
    percentage = st.slider('Orderline Percentile', 
                            min_value=0, 
                            max_value=100,
                            value=75,
                            help=_help,
                            key=report_type)
    # Daily Report
    df = ut.get_df(report_type)
    # Percentile Daily Report
    percentile_df = ut.get_df(percentile_report)
    ol_percentile_value = percentile_df.loc[percentage, N_OLS]  # Actual N orderline value
    total_days = df.shape[0]
    outside_percentile_days = df[df[N_OLS] > ol_percentile_value].shape[0]
    total_orderlines = df[N_OLS].sum()

    # Metrics
    col1, col2 = st.columns(2)
    col1.metric(f'Daily Orderlines - {percentage} Percentile', f'{int(ol_percentile_value):,}')
    col2.metric('Total Days', f'{total_days}', f'{outside_percentile_days} Days Above', delta_color='inverse')
    fig = plot.daily_bar_chart(df, ol_percentile_value)
    st.plotly_chart(fig)
    with st.expander('Stats'):
        st.table(df[N_OLS].describe().astype(int).transpose())
    st.markdown('---')

def orderlines_with_percentile_removal(report_type: str = BUSINESS_DAILY_REPORT):
    title, percentile_report = get_report_type_context(report_type)
    st.markdown(f'#### {title} - Percentile Removal')
    # Get data
    df = ut.get_df(report_type)
    percentile_df = ut.get_df(percentile_report)

    _help = """
Little explanation here :)
"""
    percentage = st.slider('Orderline Percentile To Be Removed', 
                            min_value=0, 
                            max_value=80,
                            value=5,
                            help=_help)
    ol_percentile_value = percentile_df.loc[percentage, N_OLS]  # Actual N orderline value
    total_days = df.shape[0]
    df_with_removed_ols = df[df[N_OLS] >= ol_percentile_value].copy()
    outside_percentile_days = df[df[N_OLS] < ol_percentile_value].shape[0]

    # Metrics
    col1, col2, col3 = st.columns(3)
    # Column 1
    col1_input1 = f'Daily Orderlines - {percentage} Percentile:'
    col1_input2 = f'{int(ol_percentile_value):,}'
    col1.metric(col1_input1, col1_input2)
    # Column 2
    col2_input3 = f'-{outside_percentile_days} Days Below Percentile'
    col2.metric('Total Days (Original Data):', f'{total_days}', col2_input3)
    # Column 3
    col3.metric('Calculation Performed On (Days):', f'{total_days - outside_percentile_days}')

    stats = df_with_removed_ols[N_OLS].describe().astype(int)
    fig = plot.daily_line_chart(df_with_removed_ols, stats)
    st.plotly_chart(fig)
    with st.expander('Stats'):
        st.table(stats.transpose())
    st.markdown('---')


def daily_orders(report_type: str = BUSINESS_DAILY_REPORT):
    title, _ = get_report_type_context(report_type)
    st.markdown(f'#### {title} Orders')
    df = ut.get_df(report_type)

    fig = plot.daily_order_chart(df)
    st.plotly_chart(fig)
    st.markdown('---')


def orderlines_stats(report_type: str = BUSINESS_DAILY_REPORT):
    title, _ = get_report_type_context(report_type)
    df = ut.get_df(report_type)

    st.markdown('#### Heatmaps')
    heatmap = plot.weekdays_months_heatmap(df)
    st.plotly_chart(heatmap)

    st.markdown(f'#### {title} Orderlines - BoxPlots')

    weekdays_boxplot = plot.weekdays_boxplot(df)
    st.plotly_chart(weekdays_boxplot)

    weekly_monthly_box = plot.weekdays_months_boxplot(df)
    st.plotly_chart(weekly_monthly_box)

    st.markdown('---')


def general_outbound_dashboard():

    if not ut.get_df(DAILY_REPORT) is None:
        st.markdown('### Dashboard')

        outbound_stats()

        report_type = report_type_selector()
        orderline_main_chart(report_type)
        orderlines_with_percentile_removal(report_type)
        daily_orders(report_type)
        orderlines_stats(report_type)

    else:
        no_report_yet()