import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from .settings import *
from . import utils as ut

def abc_line(dataframe: pd.DataFrame, chart_type='ORDERLINES'):
    """
    Returns an interactive graph of the ABC classification for picklines
    
    This function takes a pandas DataFrame as input and returns an interactive graph, 
    using the plotly library, showing the ABC classification of picklines. 
    The graph plots the percentage of SKUs on the x-axis and the percentage of picklines on the y-axis.
    The function calls another function `ut.get_A_class(dataframe)` to determine the percentage of class A (20% SKUs / 80% Picklines),
    it then draws a rectangle to highlight the A class on the plot. Also It subsamples the data to 300 data points to improve rendering performance.
    
    Args:
        dataframe (pd.DataFrame): DataFrame containing the report, 
                                  the columns required are "SKU_PER" and "ORDERLINES_PER"
        chart_type (str): Specify if the final report is based on picklines 'ORDERLINES' or quantity 'QTY'.
    
    Returns:
        plotly.graph_objs._figure.Figure: Returns an interactive graph, showing the ABC classification of picklines.
                                        The graph is built using the plotly library.
    """
    x = list(dataframe[SKU_PER].values)
    if chart_type == 'ORDERLINES':
        y = list(dataframe[ORDERLINES_PER].values)
        marker_color = 'blue'
        metrics_type = ORDERLINE_METRICS

    elif chart_type == 'QTY':
        y = list(dataframe[QTY_PER].values)
        marker_color = 'green'
        metrics_type = QTY_METRICS

    # Reduce data points for faster rendering
    n_datapoints_to_render = 300
    total_datapoints = len(x)
    step = total_datapoints // n_datapoints_to_render
    if step < 1:  # In case there are fewer than 300 datapoints
        step = 1
    x = x[::step]
    y = y[::step]

    sku_per, uom_per = ut.get_A_class(dataframe, chart_type)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y, name=chart_type.title(), mode='markers', hovertemplate="%{x}% SKU <br>%{y}% UoM", marker=dict(color=marker_color)))

    metrics = ut.get_abc_metrics(metrics_type)
    fig.add_shape(type="rect",
    x0=0.0, y0=0,
    x1=metrics.a_sku, y1=metrics.a_uom,
    line=dict(
        color="red",
        width=2,
        ),
    )
    fig.add_annotation( x=-.25, 
                        y=20,
                        text=f'A Class - {metrics.a_sku} / {metrics.a_uom}',
                        font=dict(color='red'),
                        textangle=270)

    fig.update_layout(  title=f'ABC Classification - {chart_type.title()}',
                        xaxis_title='SKU %',
                        yaxis_title=f'{chart_type.title()} %')

    return fig