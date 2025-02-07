import streamlit as st
import pandas as pd
import numpy as np

from .settings import *
from . import utils as ut


def create_first_pivot_table(dataframe: pd.DataFrame, selected_cols: dict):
    """The table will have ORDER_ID as index, QTY and SKU_ID as columns.
    Therefore, each row of the table will report the total quantity and the number of orderlines per order. 

    The output will be something like this:

            ORDER_ID	    QTY_SHIPPED	    SKU_ID
        0	1011244/06	    18	            8
        1	1011254/06	    18	            8
        2	1011264/06	    14	            8
        3	1011275/00	    12	            8
        4	1011275/01	    12	            8

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
    pt = dataframe.pivot_table(
                        index=selected_cols[N_ORDERS],
                        aggfunc={
                            selected_cols[QTY]:'sum', 
                            selected_cols[N_OLS]:'nunique'
                            }
                    )
    pt.reset_index(inplace=True)

    # Rename pivot table columns to consistent naming
    rename_dict = ut.renaming_dict(selected_cols)
    pt.rename(columns=rename_dict, inplace=True)

    # Convert quantity column to integer
    pt[QTY] = pt[QTY].astype(int)
    return pt


def create_general_report(
                    first_pt: pd.DataFrame, 
                    selected_cols: dict, 
                    groupby: str, 
            ):

    # 1. Generate grouped report
    pt_params = ut.groupby_params(groupby)
    report = first_pt.pivot_table(**pt_params)

    # Get totals
    first_col_total = report.sum().iloc[0]
    second_col_total = report.sum().iloc[1]

    ## Generate cumulative sum table
    cumsum_report = report.cumsum()
    ut.append_to_colname(cumsum_report, '_CS')

    ## Concatenate cumulative sum table with original report
    report_w_cs = pd.concat([report, cumsum_report], axis=1)

    ## Create dataframe divisor to compute percentages
    first_col = [first_col_total for x in range(report.shape[0])]
    second_col = [second_col_total for x in range(report.shape[0])]
    data = np.matrix([first_col, second_col, first_col, second_col,]).transpose()
    divisor_df = pd.DataFrame(index=report_w_cs.index, data=data, columns=report_w_cs.columns)

    ## Compute percentages actual and cumulative
    report_percentage = np.round(report_w_cs.divide(divisor_df, axis=1) * 100, 2)
    ut.append_to_colname(report_percentage, '_%')

    ## Create final report
    final_report = pd.concat([report_w_cs, report_percentage],axis=1)
    return final_report

def create_one_orderline_report(dataframe: pd.DataFrame):
    ol1 = dataframe.pivot_table(index=[N_OLS, QTY,], aggfunc={N_ORDERS:'nunique',}).reset_index(-1)
    ol1 = ol1.loc[1, :].sort_values(QTY)
    return ol1



def whole_dataset_report(dataframe: pd.DataFrame, selected_cols: dict,):
    st.markdown('### Full Dataset Report')
    with st.expander('More Info'):
        text = """
        This will create two reports:

        1. Quantity
        2. Orderlines

        The dataset is first grouped by unique **order** number.
        Then for each order, the total quantity is summed and the number of unique SKUs is counted.  

        For example:

        |  ORDER_ID | QTY_SHIPPED | SKU_ID |
        |----------:|------------:|-------:|
        | 325617586 |        94.0 |     10 |
        | 325617587 |       435.0 |     26 |
        | 325617588 |      2350.0 |     52 |
        | 337727697 |       266.0 |     35 |
        | 340093936 |       158.0 |     10 |


        Based on this information, quantity and orderline reports are generated as next step.
        """
        st.markdown(text)

    # Genrate reports
    if st.button('Create Report', key='whole_report'):
        with st.spinner('Creating report...'):

            # Create first pivot table with order id as index
            first_pt = create_first_pivot_table(dataframe, selected_cols)
            ut.save_df(first_pt, FIRST_PT)

            # Create report with quantity as index
            qty_report = create_general_report(first_pt, selected_cols, groupby='quantity')
            ut.save_df(qty_report, QTY_REPORT)

            # Create report with N orderlines as index
            ol_report = create_general_report(first_pt, selected_cols, groupby='orderline')
            ut.save_df(ol_report, OL_REPORT)

            # Create one-orderline report
            ol_one = create_one_orderline_report(first_pt)
            ut.save_df(ol_one, ONE_OL)

        st.success('Done! Click on the Dashboard tab to view the report.')

    st.markdown('---')


# UNUSED
def specific_group_report(dataframe: pd.DataFrame, selected_cols: dict,):
    st.markdown('### Group By Report')
    with st.expander('More Info'):
        text = """
        Brief Explanation Here
        """
        st.markdown(text)
    if st.button('Create Report', key='specific_report'):
        ...