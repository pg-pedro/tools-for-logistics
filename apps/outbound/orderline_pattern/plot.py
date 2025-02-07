import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd

from .settings import *
from . import utils as ut

def qty_pie_with_slider_alt(dataframe: pd.DataFrame, ):
    value = st.slider('Up to quantity', 1, 25, 5)

    # Selected range
    inner_values_df = dataframe.loc[:value]
    # Outer range
    outer_values_df = dataframe.loc[value+1:].sum()

    labels = list(inner_values_df.index) + [f'{value+1}+']
    pull = [0 for x in labels]
    pull[-1] = .2
    values = list(inner_values_df[N_OLS].values) + [outer_values_df.loc[N_OLS]]
    qty_fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull, sort=False)])

    values = list(inner_values_df[N_ORDERS].values) + [outer_values_df.loc[N_ORDERS]]
    order_fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull, sort=False)])

    col1, col2 = st.columns(2)
    col1.plotly_chart(qty_fig, use_container_width=True)
    col2.plotly_chart(order_fig, use_container_width=True)

def dataset_metrics():
    first_pt = ut.get_df(FIRST_PT)
    # Get totals
    total_qty = first_pt[QTY].sum()
    total_ol = first_pt[N_OLS].sum()
    total_orders = first_pt.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric('Orders', f'{total_orders:,}', )
    col2.metric('Total Orderlines', f'{total_ol:,}', )
    col3.metric('Total Units', f'{total_qty:,}', )


def qty_pie_with_slider(dataframe: pd.DataFrame, ):
    value = st.slider('Up to quantity:', 1, 25, 5)
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['Orderlines', 'Orders'])

    # Selected range
    inner_values_df = dataframe.loc[:value]
    # Outer range
    outer_values_df = dataframe.loc[value+1:].sum()

    labels = list(inner_values_df.index) + [f'{value+1}+']
    pull = [0 for x in labels]
    pull[-1] = .12
    ol_values = list(inner_values_df[N_OLS].values) + [outer_values_df.loc[N_OLS]]
    ol_values = [int(x) for x in ol_values]
    order_values = list(inner_values_df[N_ORDERS].values) + [outer_values_df.loc[N_ORDERS]]
    order_values = [int(x) for x in order_values]

    # Orderline Pie Chart
    fig.add_trace(go.Pie(labels=labels, 
                         values=ol_values, 
                         pull=pull, 
                         sort=False,
                         name='Orderlines',
                         hovertemplate='Quantity: <b>%{label}</b>: <br><br>Orderlines:<br><b>%{value}</b> - %{percent}'),
                1,1)
    # Order Pie Chart
    fig.add_trace(go.Pie(labels=labels, 
                         values=order_values, 
                         pull=pull, 
                         sort=False,
                         name='Orders',
                         hovertemplate='Quantity: <b>%{label}</b>: <br><br>Orders:<br><b>%{value}</b> - %{percent}'),
                1,2)
    
    fig.update_layout(legend_title_text='Quantity')

    st.plotly_chart(fig, use_container_width=False)


def orderline_pie_with_slider():
    value = st.slider('Up to N Orderlines:', 1, 25, 5)
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['Quantity', 'Orders'])

    # Get orderline report from session state
    dataframe = ut.get_df(OL_REPORT)

    # Selected range
    inner_values_df = dataframe.loc[:value]
    # Outer range
    outer_values_df = dataframe.loc[value+1:].sum()

    labels = list(inner_values_df.index) + [f'{value+1}+']
    pull = [0 for x in labels]
    pull[-1] = .12
    qty_values = list(inner_values_df[QTY].values) + [outer_values_df.loc[QTY]]
    qty_values = [int(x) for x in qty_values]
    order_values = list(inner_values_df[N_ORDERS].values) + [outer_values_df.loc[N_ORDERS]]
    order_values = [int(x) for x in order_values]

    # Quantity Pie Chart
    fig.add_trace(go.Pie(labels=labels, 
                         values=qty_values, 
                         pull=pull, 
                         sort=False,
                         name='Quantity',
                         hovertemplate='Orderlines: <b>%{label}</b>: <br><br>Quantity:<br><b>%{value}</b> - %{percent}',
                         ),
                    1,1)
    # Order Pie Chart
    fig.add_trace(go.Pie(labels=labels, 
                         values=order_values, 
                         pull=pull, 
                         sort=False,
                         name='Orders',
                         hovertemplate='Orderlines: <b>%{label}</b>: <br><br>Orders:<br><b>%{value}</b> - %{percent}',
                         ),
                    1,2)
    
    fig.update_layout(legend_title_text='Orderlines', )

    st.plotly_chart(fig, use_container_width=False)

def orderline_bar_with_slider():
    fig = go.Figure()
    value = st.slider('Up to N Orderlines:', 1, 50, 10, key='bar_chart')

    # Get orderline report from session state
    dataframe = ut.get_df(OL_REPORT)

    # Selected range
    inner_values_df = dataframe.loc[:value]
    # Outer range
    outer_values_df = dataframe.loc[value+1:].sum()

    labels = list(inner_values_df.index) + [f'{value+1}+']

    # Orders Cumulative
    order_cs_values = inner_values_df[f'{N_ORDERS}_CS_%'].values
    fig.add_trace(go.Bar(
        x=labels,
        y=order_cs_values,
        name='Orders Cumulative %',
        hovertemplate='Orderline: %{x} <br>Order Cumulative: %{y}%'
    ))

    # Orders %
    order_per_values = inner_values_df[f'{N_ORDERS}_%'].values
    fig.add_trace(go.Bar(
        x=labels,
        y=order_per_values,
        name='Orders %',
        hovertemplate='Orderline: %{x} <br>Order Actual: %{y}%'
    ))

    fig.update_layout(  barmode='group',
                        xaxis_title='N Orderlines',
                        yaxis_title='Orders %',)

    st.plotly_chart(fig)


def orderline_custom_inner_group(df: pd.DataFrame, lower: int, upper: int):
    # Data preparation
    ## Left range from 1 to lower bound minus 1
    left_range = [i for i in range(1, lower)]
    left_df = df.filter(items=left_range, axis=0)
    ## Inner from lower bound to upper bound
    inner_range = [i for i in range(lower, upper+1)]
    inner_df = df.filter(items=inner_range, axis=0)
    ## Outer range from upper plus 1 till dataframe end
    df_end = df.index[-1]
    right_range = [i for i in range(upper+1, df_end+1)]
    right_df = df.filter(items=right_range, axis=0)
    # Create chart
    # fig = go.Figure()
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['Quantity', 'Orders'])
    ## Labels
    left_label = list(left_df.index)
    left_label = [f'Up to {lower - 1}']
    inner_label = [f'{lower} - {upper}']
    right_label = [f'{upper+1}+']
    labels = left_label + inner_label + right_label
    ## Pull
    pull = [0 for x in labels]
    pull[-2] = .12
    ## Order values
    left_orders = [left_df[N_ORDERS].sum()]
    inner_orders = [inner_df[N_ORDERS].sum()]
    right_orders = [right_df[N_ORDERS].sum()]
    order_values = left_orders + inner_orders + right_orders
    ## Quantity values
    left_qty = [left_df[QTY].sum()]
    inner_qty = [inner_df[QTY].sum()]
    right_qty = [right_df[QTY].sum()]
    qty_values = left_qty + inner_qty + right_qty

    # Quantity Pie Chart
    fig.add_trace(go.Pie(labels=labels, 
                         values=qty_values, 
                         pull=pull, 
                         sort=False,
                         name='Quantity',
                         hovertemplate='Orderlines: <b>%{label}</b>: <br><br>Quantity:<br><b>%{value}</b> - %{percent}',
                         ),
                    1,1)
    # Order Pie Chart
    fig.add_trace(go.Pie(labels=labels, 
                         values=order_values, 
                         pull=pull, 
                         sort=False,
                         name='Orders',
                         hovertemplate='Orderlines: <b>%{label}</b>: <br><br>Orders:<br><b>%{value}</b> - %{percent}',
                         ),
                    1,2)
    
    fig.update_layout(legend_title_text='Orderlines', )
    return fig

def equally_spaced_ol_range_plot(df: pd.DataFrame, n_groups: int, barmode: str = 'group'):
    max_ols = max(df.index)
    # Inner grouping
    groups = [2] + [i*5 for i in range(1, n_groups)]
    labels = ['2'] + [f'2 - {i*5}' for i in range(1, n_groups)]
    # Order traces
    ## Single orderline orders
    single_ol_orders = df.loc[1, N_ORDERS]
    single_ol_orders_per = df.loc[1, N_ORDERS_PER]
    n_order_single = [single_ol_orders_per for i in range(1, n_groups+1)]
    single_text =   f'<b>Orderlines</b>: 1<br>' + \
                    f'<b>Total Orders</b>: {single_ol_orders} - {round(single_ol_orders_per, 2)}%'
    ## Inner group
    n_order_inner = []
    inner_text = []
    ## Outer group
    n_order_outer = []
    outer_text = []
    
    for group in groups:
        # Orders
        ## Inner orders
        items = [i for i in range(2, group+1)]
        total_inner_orders_per = df.filter(items=items, axis=0)[N_ORDERS_PER].sum()
        total_inner_orders = df.filter(items=items, axis=0)[N_ORDERS].sum()
        n_order_inner.append(total_inner_orders_per)
        text =  f'<b>Orderlines</b>: 2 - {items[-1]}<br>' + \
                f'<b>Total Orders</b>: {total_inner_orders} - {round(total_inner_orders_per, 2)}%'
        inner_text.append(text)

        ## Outer orders
        items = [i for i in range(group+1, max_ols+1)]
        total_outer_orders_per = df.filter(items=items, axis=0)[N_ORDERS_PER].sum()
        total_outer_orders = df.filter(items=items, axis=0)[N_ORDERS].sum()
        n_order_outer.append(total_outer_orders_per)
        text =  f'<b>Orderlines</b>: {items[0]} - {items[-1]}<br>' + \
                f'<b>Total Orders</b>: {total_outer_orders} - {round(total_outer_orders_per, 2)}%'
        outer_text.append(text)
    
    # Create stacked bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=n_order_single, name='1', hovertext=single_text, hoverinfo='text'))
    fig.add_trace(go.Bar(x=labels, y=n_order_inner, name='Inner Group', hovertext=inner_text, hoverinfo='text'))
    fig.add_trace(go.Bar(x=labels, y=n_order_outer, name='Outer Group', hovertext=outer_text, hoverinfo='text'))

    fig.update_layout(  barmode=barmode, 
                        title='Orders Vs. Orderlines', 
                        legend_title_text='Orderlines', 
                        xaxis_title='Inner Group', 
                        yaxis_title='Orders %')

    return fig

    ...

def one_orderline_pie_with_slider():
    value = st.slider('Up to quantity:', 1, 15, 5)
    fig = go.Figure()

    # Get orderline report from session state
    dataframe = ut.get_df(ONE_OL)
    df = dataframe.set_index(QTY)

    # Selected range
    inner_values_df = df.loc[:value]
    # Outer range
    outer_values_df = df.loc[value+1:].sum()

    labels = list(inner_values_df.index) + [f'{value+1}+']
    
    pull = [0 for x in labels]
    pull[0] = .12
    order_values = list(inner_values_df[N_ORDERS].values) + [outer_values_df.loc[N_ORDERS]]
    order_values = [int(x) for x in order_values]

    fig.add_trace(go.Pie(labels=labels, values=order_values, pull=pull, sort=False))
    
    fig.update_layout(legend_title_text='Quantity', title='One-orderline orders')

    st.plotly_chart(fig, use_container_width=True)