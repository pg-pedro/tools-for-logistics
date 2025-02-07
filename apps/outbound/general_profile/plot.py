from calendar import day_name, month_abbr

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np

from .settings import *
from . import utils as ut

def daily_bar_chart(df: pd.DataFrame, ol_percentile_value: int):
    # Get data
    x = df.index
    y = df[N_OLS].to_numpy()
    trend_line = ut.get_trend_line(y)
    # PlotlyBar Chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name='Daily Orderlines',
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=trend_line,
        name='Trend',
        line = dict(dash='dash')
    ))

    fig.add_hrect(y0=0, y1=ol_percentile_value, line_width=0, fillcolor="green", opacity=.12)
    fig.add_hline(ol_percentile_value)

    fig.update_layout(  title='N Daily Orderlines',
                        xaxis_title='Date',
                        yaxis_title='N Orderlines')

    return fig

def daily_line_chart(df: pd.DataFrame, stats: pd.Series):
    # Get data
    x = df.index
    y = df[N_OLS].to_numpy()
    mean = [stats.loc['mean'] for i in x]
    median = [stats.loc['50%'] for i in x]
    third_quartile = [stats.loc['75%'] for i in x]


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name='OLs',
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=mean,
        name='Mean',
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=median,
        name='Median',
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=third_quartile,
        name='Third Quartile',
    ))


    fig.update_layout(  title='Daily Orderlines After Removal',
                        xaxis_title='Date',
                        yaxis_title='N Orderlines')
    return fig


def daily_order_chart(df: pd.DataFrame, ):
    # Get data
    x = df.index
    y = df[N_ORDERS].to_numpy()
    trend_line = ut.get_trend_line(y)


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name='N Orders',
        ), 
    )
    fig.add_trace(go.Scatter(
        x=x,
        y=trend_line,
        name='Trend',
        line = dict(dash='dash')
    ))

    fig.update_layout(  title='N Daily Orders',
                        xaxis_title='Date',
                        yaxis_title='N Orders')
    return fig



def weekdays_boxplot(df: pd.DataFrame):
    fig =  px.box(df, x=DAYS, y=N_OLS)
    fig.update_layout(title='Weekday Orderlines')
    return fig

def weekdays_months_boxplot(df: pd.DataFrame):
    fig =  px.box(df, x=DAYS, y=N_OLS, color=MONTHS)
    fig.update_layout(title='Monthly Weekday Orderlines')
    return fig

def weekdays_months_heatmap(df: pd.DataFrame):
    function = st.selectbox(
                'Select Aggregation Function', 
                options=['mean', 'median', 'std', 'min', 'max'], 
                format_func=lambda x: x.title(),
                index=1)
    pt = df.pivot_table(index=DAYS, columns=MONTHS, aggfunc={N_OLS:function}).droplevel(0, axis=1)
    # Sort weekdays
    pt = pt.filter(items=list(day_name), axis=0)

    # Sort Months
    sorting_dict = dict()
    for i, m in enumerate(month_abbr):
        sorting_dict[m] = i
    cols = pt.columns
    cols = sorted(cols, key= lambda m: sorting_dict[m])
    pt = pt[cols].copy()
    fig = px.imshow(pt.to_numpy(), 
                    labels=dict(x='Months', y='Day of Week', color=f'{function.title()} OLs'),
                    x=pt.columns, 
                    y=pt.index,
                    text_auto=True,
                    color_continuous_scale='Greys')
    fig.update_layout(title=f'{function.title()} Daily Orderlines')
    return fig