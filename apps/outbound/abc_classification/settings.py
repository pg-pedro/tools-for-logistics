# Root session state dict key
## Everything else will be save under this one

"""
ABC_CLASS: This is the root key of the session state that contains all the other keys used in the Streamlit application.
FIRST_PIVOT: This is the key that stores the first pivot table that is generated in the data analysis process.
ORDERLINE_REPORT: This is the key that stores the final pickline report, which is generated after the first pivot table is processed.
FULL_REPORT: This is the key that stores the full report, which is generated after the first pivot table and final pickline report are merged.
QTY: This is the column name for the quantity of items picked in the dataframe.
ORDERLINES: This is the column name for the number of picklines in the dataframe.
ORDERLINES_PER: This is the column name for the percentage of picklines in the dataframe.
N_ORDERS: This is the column name for the number of orders in the dataframe.
SKU_ID: This is the column name for the SKU ID in the dataframe.
SKU_PER: This is the column name for the percentage of SKUs in the dataframe.

This constants should be used consistently throughout the project, as they are used to index/retrieve dataframe and keys.
"""
ABC_CLASS = 'abc_classification'
FIRST_PIVOT = 'first_pt'
ORDERLINE_REPORT = 'orderline_report'
QTY_REPORT = 'qty_report'
FULL_REPORT_ORDERLINES = 'full_report_orderlines'
FULL_REPORT_QTY = 'full_report_qty'

ORDERLINE_METRICS = 'orderline_metrics'
QTY_METRICS = 'qty_metrics'

QTY = 'QTY_PICKED'
ORDERLINES = 'OLs'
ORDERLINES_PER = f'{ORDERLINES}_%'
QTY_PER = f'{QTY}_%'
N_ORDERS = 'N_ORDERS'
SKU_ID = 'SKU_ID'
SKU_PER = 'SKU_%'
ABC_COL = 'ABC_CLASS'
