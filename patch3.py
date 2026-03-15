import re

file_path = "apps/outbound/orderline_pattern/orderline_pattern backup.py"
with open(file_path, "r") as f:
    content = f.read()

# Replace the slower divisor approach with broadcasting
new_content = re.sub(
    r"            # Create dataframe divisor to compute percentages\n            ol_col = \[total_ol for x in range\(qty_report\.shape\[0\]\)\]\n            orders_col = \[total_orders for x in range\(qty_report\.shape\[0\]\)\]\n            data = np\.matrix\(\[ol_col, orders_col, ol_col, orders_col,\]\)\.transpose\(\)\n            divide_df = pd\.DataFrame\(index=qty_report_w_cs\.index, data=data, columns=qty_report_w_cs\.columns\)\n\n            # Compute percentages actual and cumulative\n            qty_report_percentage = np\.round\(qty_report_w_cs\.divide\(divide_df, axis=1\) \* 100, 2\)",
    r"""            # Compute percentages actual and cumulative using broadcasting
            divisor_series = pd.Series([total_ol, total_orders, total_ol, total_orders], index=qty_report_w_cs.columns)
            qty_report_percentage = np.round(qty_report_w_cs.divide(divisor_series, axis=1) * 100, 2)""",
    content,
    flags=re.MULTILINE
)

with open(file_path, "w") as f:
    f.write(new_content)
