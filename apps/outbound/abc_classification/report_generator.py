import streamlit as st
import pandas as pd

from .settings import *
from . import utils as ut

def first_pivot(dataframe: pd.DataFrame, selected_cols: dict):
    """Creates the first table to be used later to compute ABC classification.

    This function takes a pandas DataFrame and a dictionary of selected columns as inputs. It groups the data in the input dataframe
    by order ID and SKU ID, counts the number of pick-lines and sums up the quantities picked for each unique order-SKU combination.
    It then creates a new pivot table with columns for number of orders, number of picklines, and total quantity picked, indexed
    by the SKU ID. It then drops the multi-level columns, renames columns according to the selected_cols dictionary, 
    Computes the percentage of SKU and picklines and 
    computes total number of picklines and quantity picked per SKU, counts the unique number of order IDs per SKU.
    Finally, it converts the quantity column to integer values.
    The final pivot table is then returned.

    The output will be something like this:

                    	N_ORDERS	N_ORDERLINESS	QTY_PICKED
        SKU_ID			
        1346751-001-LG	7250	    7252	        154135
        1357096-001-MD	4911	    4927	        15726
        1357096-001-LG	4655	    4682	        14968
        1306443-001-LG	4533	    4546	        86542
        1346751-100-LG	4504	    4505	        138816

    Args:
        dataframe (pd.DataFrame): Dataframe containing the order data, 
                                  must include columns specified in the selected_cols dictionary
                                  
        selected_cols (dict): Dictionary containing the relevant column as values.
                              { 'N_ORDERS':'ORDER_ID',
                                'SKU_ID':'SKU_ID',
                                'QTY':'QTY_PICKED'}
                              where 'N_ORDERS' is the name of the column for order ids, 'SKU_ID' is the name of the column for sku ids,
                              'QTY' is the name of the column for quantities
                              
    Returns:
        pd.DataFrame: The final pivot table, with columns for number of orders, number of picklines, and total quantity picked, 
                      indexed by the SKU ID.
    """
    # Group data by ORDER_ID and SKU_ID and count orderlines and sum up picked quantities
    pt = dataframe.pivot_table(
                index=[selected_cols[N_ORDERS], selected_cols[SKU_ID]], 
                aggfunc={selected_cols[QTY]:'sum'}
            )
    pt[ORDERLINES] = 1
    # Drop multilevel column
    pt.reset_index(inplace=True)

    # Rename columns
    renaming_dict = ut.renaming_dict(selected_cols)
    renaming_dict.update({'sum':QTY})
    pt.rename(columns=renaming_dict, inplace=True)

    # st.dataframe(pt.head())

    # Sum up total pick-lines and quantity picked per sku, count unique order id per sku
    pt = pt.pivot_table(index=SKU_ID, 
                        aggfunc={   ORDERLINES:'sum', 
                                    QTY:'sum', 
                                    N_ORDERS:'nunique'}).reset_index()
    # Quantity column to Integer
    pt[QTY] = pt[QTY].astype(int)
    return pt

def create_final_orderline_report(dataframe: pd.DataFrame):
    """
    Returns a final report for picklines 
    
    This function takes a pandas DataFrame as input and returns a final report of picklines in the form of a pandas dataframe.
    The function sorts the input dataframe by picklines and quantity in descending order, adds a 'SKU_PER' column to the dataframe
    and computes the cumulative sum of this column and picklines. It then computes the total number of SKUs and total number of 
    picklines and it uses these values to compute the percentages of SKUs and picklines in the final report. The result dataframe
    is rounded to 2 decimal places and returned.
   
    Args:
        dataframe (pd.DataFrame): DataFrame containing the report, 
                                  the columns required are "ORDERLINES","QTY" and "SKU_ID"
    
    Returns:
        pd.DataFrame: The final report of picklines, with columns "SKU_PER" and "ORDERLINES_PER" and their respective percentages.
    """
    # Sort from largest to smallest on number of picklines and quantity
    pt = dataframe.sort_values([ORDERLINES, QTY], ascending=False)
    pt.set_index(SKU_ID, inplace=True)
    pt[SKU_PER] = 1  # Will store SKU percentage

    abc_cols = [SKU_PER, ORDERLINES]
    pt_cumsum = pt[abc_cols].cumsum()

    # Compute totals
    total_sku = pt.shape[0]
    total_picklines = pt[ORDERLINES].sum()

    # Compute percentages
    pt_final = pt_cumsum.divide([total_sku, total_picklines])
    pt_final = round(pt_final * 100, 2)
    return pt_final

def create_qty_report(dataframe: pd.DataFrame):
    """
    Returns a final report for sku quantity. 
    
    This function takes a pandas DataFrame as input and returns a final report of picklines in the form of a pandas dataframe.
    The function sorts the input dataframe by picklines and quantity in descending order, adds a 'SKU_PER' column to the dataframe
    and computes the cumulative sum of this column and picklines. It then computes the total number of SKUs and total number of 
    picklines and it uses these values to compute the percentages of SKUs and picklines in the final report. The result dataframe
    is rounded to 2 decimal places and returned.
   
    Args:
        dataframe (pd.DataFrame): DataFrame containing the report, 
                                  the columns required are "ORDERLINES","QTY" and "SKU_ID"
    
    Returns:
        pd.DataFrame: The final report of quantity, with columns "SKU_PER" and "ORDERLINES_PER" and their respective percentages.
    """
    # Sort from largest to smallest on number of picklines and quantity
    pt = dataframe.sort_values([QTY, ORDERLINES], ascending=False)
    pt.set_index(SKU_ID, inplace=True)
    pt[SKU_PER] = 1  # Will store SKU percentage

    abc_cols = [SKU_PER, QTY]
    pt_cumsum = pt[abc_cols].cumsum()

    # Compute totals
    total_sku = pt.shape[0]
    total_quantity = pt[QTY].sum()

    # Compute percentages
    pt_final = pt_cumsum.divide([total_sku, total_quantity])
    pt_final = round(pt_final * 100, 2)
    return pt_final

def create_full_report(first_pivot: pd.DataFrame, report: pd.DataFrame, report_type: str = 'ORDERLINES'):
    """
    Creates a full report containing all relevant data for the ABC analysis by merging two input dataframes.

    This function takes two input dataframes, a "first_pivot" table and a "report" table, and merge them on their 
    SKU_ID column. The merged dataframe is sorted by number of picklines and total quantity picked.
    The final merged dataframe is then returned.

    Args:
        first_pivot (pd.DataFrame): The pivot table containing information on the number of orders, number of picklines,
                                   and total quantity picked per SKU, indexed by the SKU ID.
        report (pd.DataFrame): The pivot table containing information on the percentage of SKU and picklines
                                       indexed by the SKU ID.
        report_type (str): Specify if the final report is based on picklines 'ORDERLINES' or quantity 'QTY'.

    Returns:
        pd.DataFrame: The final merged dataframe containing all relevant data for the ABC analysis.
    """
    pt = first_pivot.set_index(SKU_ID)
    merged=  pt.merge(  report,
                        left_index=True, 
                        right_index=True,
                        suffixes=('', '_%'))
    if report_type == 'ORDERLINES':
        merged.sort_values([ORDERLINES, QTY], ascending=False, inplace=True)
    elif report_type =='QTY':
        merged.sort_values([QTY, ORDERLINES, ], ascending=False, inplace=True)
    else:
        Exception('Unknown report type. Please specify either "ORDERLINES" or "QTY".')
    return merged


def create_abc_orderline_report(dataframe: pd.DataFrame, selected_cols: dict):
    """
    Generates an ABC classification report for picklines and displays it in the Streamlit app.

    This function takes a dataframe and a dictionary of selected columns as input and generates an ABC classification report
    for picklines. It first calls the 'first_pivot' function to create a pivot table, then calls the 'create_final_orderline_report'
    to create a pickline report, and finally calls the 'create_full_report' function to merge the two reports. The final
    merged report is then displayed in the Streamlit app, and a button is provided to create the report.

    Args:
        dataframe (pd.DataFrame): The dataframe containing the orderline data.
        selected_cols (dict): Dictionary containing the relevant column as values.
    """
    st.markdown('### ABC Classification')
    with st.expander('More Info'):
        text = """
        This classification is based on the SKU's number of pick-lines.
        """
        st.markdown(text)

    # Genrate reports
    if st.button('Create Report', key='ORDERLINE_REPORT'):
        with st.spinner('Creating report...'):

            # Create first pivot table with order id as index
            pt = first_pivot(dataframe, selected_cols)
            ut.save_df(pt, FIRST_PIVOT)

            # Create pick-line report
            ol_report = create_final_orderline_report(pt)
            ut.save_df(ol_report, ORDERLINE_REPORT)

            # Create quantity report
            qty_report = create_qty_report(pt)
            ut.save_df(qty_report, QTY_REPORT)

            # Create merged pickline report
            merged_report = create_full_report(pt, ol_report)
            ut.save_df(merged_report, FULL_REPORT_ORDERLINES)

            # Create merged qty report
            merged_report = create_full_report(pt, qty_report, report_type='QTY')
            ut.save_df(merged_report, FULL_REPORT_QTY)

        st.success('Done! Click on the Dashboard tab to view the report.')
    st.markdown('---')

    

    