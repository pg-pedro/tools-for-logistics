import re

file_path = "apps/outbound/orderline_pattern/orderline_pattern backup.py"
with open(file_path, "r") as f:
    content = f.read()

# Replace the slower divisor approach with broadcasting
new_content = re.sub(
    r"            first_col = \[first_col_total for x in range\(qty_report_w_cs\.shape\[0\]\)\]\n            second_col = \[second_col_total for x in range\(qty_report_w_cs\.shape\[0\]\)\]\n            data = np\.matrix\(\[first_col, second_col, first_col, second_col,\]\)\.transpose\(\)\n            divide_df = pd\.DataFrame\(index=qty_report_w_cs\.index, data=data, columns=qty_report_w_cs\.columns\)\n\n            qty_report_percentage = np\.round\(qty_report_w_cs\.divide\(divide_df, axis=1\) \* 100, 2\)",
    r"""            ## Compute percentages actual and cumulative using broadcasting
            divisor_series = pd.Series([first_col_total, second_col_total, first_col_total, second_col_total], index=qty_report_w_cs.columns)
            qty_report_percentage = np.round(qty_report_w_cs.divide(divisor_series, axis=1) * 100, 2)""",
    content,
    flags=re.MULTILINE
)

with open(file_path, "w") as f:
    f.write(new_content)
