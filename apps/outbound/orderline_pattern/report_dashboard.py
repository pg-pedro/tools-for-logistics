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

def orderline_custom_inner_group():
    selection =  st.slider('Select Orderline Grouping Range:', min_value=2, max_value=50, value=(2,10))
    # Get orderline report from session state
    df = ut.get_df(OL_REPORT)
    fig = plot.orderline_custom_inner_group(df, selection[0], selection[1])
    st.plotly_chart(fig)

def equally_spaced_ol_range():
    st.markdown('#### Orderlines - Custom Range')
    with st.expander('More Info'):
        text = """
        
        """
        st.markdown(text)
    df = ut.get_df(OL_REPORT)
    n_groups = st.slider('Number of Groups:', min_value=2, max_value=12, value=7)
    fig = plot.equally_spaced_ol_range_plot(df, n_groups)
    st.plotly_chart(fig)

    fig = plot.equally_spaced_ol_range_plot(df, n_groups, 'stack')
    st.plotly_chart(fig)

    st.markdown('---')

# def group_of_sliders():
#     if 'ol_selection' not in st.session_state[OL_PATTERN]:
#         st.session_state[OL_PATTERN]['ol_selection'] = [-1]

#     slider_container = st.empty()
    
#     last_selected = st.session_state[OL_PATTERN]['ol_selection']
#     starting_range = [2, 7]
#     max_value = 30
#     custom_range = ut.custom_range()

#     if len(custom_range) <= 0:
#         slider_range = starting_range
#         last_selected[0] = starting_range[1]
#         minus_button_disabled = False
#     else:
#         slider_range = [custom_range[-1][1]+1, custom_range[-1][1]+5]
#         minus_button_disabled = False

#     col1, col2, col3, col4, _ = st.columns([3,1,1,1,10], )
#     col1.markdown('Add Group:')
#     plus_button = col2.button('+')
#     minus_button = col3.button('-', disabled=minus_button_disabled)
#     reset_button = col4.button('Reset', help='Press twice to refresh the slider')


#     selection = slider_container.slider( 
#                                         'Select Orderline Grouping Range:', 
#                                         min_value=slider_range[0], 
#                                         max_value=max_value, 
#                                         value=slider_range[1], 
#                                         key='group-of-sliders'
#                                 )

#     if reset_button:
#         custom_range.clear()
#         print(custom_range)

#     if plus_button:
#         custom_range.append([slider_range[0], selection])
#         slider_range = [selection, selection+5]
#         print(slider_range)
#         print(custom_range)
#         # Slider Re-render
#         with slider_container.container():
#             selection = st.slider( 
#                                     'Select Orderline Grouping Range:', 
#                                     min_value=slider_range[0], 
#                                     max_value=max_value, 
#                                     value=slider_range[1], 
#                             )

#     if minus_button:
#         if len(custom_range) > 0:
#             _ = custom_range.pop()  

#         # Slider Re-render
#         if len(custom_range) <= 0:
#             slider_range = [starting_range[0], selection]
#         else:
#             slider_range = [custom_range[-1][1]+1, custom_range[-1][1]+5]
#         with slider_container.container():
#             selection = st.slider( 
#                                     'Select Orderline Grouping Range:', 
#                                     min_value=slider_range[0], 
#                                     max_value=max_value, 
#                                     value=slider_range[1], 
#                             )
#         print(custom_range)

#     print(f'Output: {custom_range + [[custom_range[-1][1]+1 if len(custom_range)>0 else starting_range[0], selection]]}')

def orderline_dashboard():
    st.markdown('#### Orderlines')
    with st.expander('More Info'):
        text = """
        The dataset is first grouped by unique **order** number.
        Then for each order, the total quantity is summed and the number of unique SKUs - *orderlines* is counted. 

        Next step is to group by orderline. 

        | Order Total Orderlines | N_ORDERS | QTY     | N_ORDERS_% |  QTY_% |
        |:----------------------:|:--------:|:-------:|:----------:|:------:|
        |            1           |   788520 | 966324  |    70.57   | 7.85   |
        |            2           |   109993 | 367259  |     9.84   | 2.98   |
        |            3           |    32645 | 505985  |     2.92   | 4.11   |
        |            4           |    24797 | 584471  |     2.22   | 4.75   |
        |            5           |    22793 | 1230477 |     2.04   | 9.99   |
        |            6           |    23378 | 865457  |     2.09   | 7.03   |
        """
        st.markdown(text)
    plot.orderline_pie_with_slider()

    st.markdown('#### Orderlines - Custom Range')
    with st.expander('More Info'):
        text = """
        
        """
        st.markdown(text)
    orderline_custom_inner_group()
    st.markdown('---')

    equally_spaced_ol_range()

def one_orderline_dashboard():
    st.markdown('#### One Orderline')

    with st.expander('More Info'):
        text = """
        This pie chart shows what **one-orderline** orders are like, in terms of quantity. 
        """
        st.markdown(text)
    plot.one_orderline_pie_with_slider()
    st.markdown('---')

def dataset_metrics_dashboard():
    st.markdown('#### Overall Outbound Info')
    plot.dataset_metrics()
    st.markdown('---')

def quantity_dashboard():
    st.markdown('#### Quantity')
    with st.expander('More Info'):
        text = """
        The dataset is first grouped by unique **order** number.
        Then for each order, the total quantity is summed and the number of unique SKUs - *orderlines* is counted. 

        Next step is to group by quantity. 

        | Order Total Qty |  N_OLS | N_ORDERS | N_OLS_% | N_ORDERS_% |
        |:---------------:|:------:|:--------:|:-------:|:----------:|
        |        1        | 780983 |   780983 | 22.84   |    69.90   |
        |        2        | 212770 |   108574 |  6.22   |     9.72   |
        |        3        |  83022 |    28937 |  2.43   |     2.59   |
        |        4        |  60419 |    16358 |  1.77   |     1.46   |
        |        5        |  43264 |     9791 |  1.27   |     0.88   |
        |        6        |  66614 |    13533 |  1.95   |     1.21   |
        |        7        |  48003 |     8256 |  1.40   |     0.74   |
        """
        st.markdown(text)
    df = ut.get_df(QTY_REPORT)
    plot.qty_pie_with_slider(df)
    st.markdown('---')

def orderline_cumulative():
    st.markdown('#### Orderline - Cumulative')
    with st.expander('More Info'):
        text = """

        """
        st.markdown(text)
    plot.orderline_bar_with_slider()


def whole_dataset_dash():

    if not ut.get_df(FIRST_PT) is None:
        st.markdown('### Dashboard')

        dataset_metrics_dashboard()

        orderline_dashboard()

        one_orderline_dashboard()

        orderline_cumulative()

        quantity_dashboard()

    else:
        no_report_yet()
