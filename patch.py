import re

file_path = "apps/outbound/orderline_pattern/report_generator.py"
with open(file_path, "r") as f:
    content = f.read()

# Replace the slower divisor approach with broadcasting
new_content = re.sub(
    r"    first_col = \[first_col_total for x in range\(len\(report\)\)\]\n    second_col = \[second_col_total for x in range\(len\(report\)\)\]\n    data = np\.matrix\(\[first_col, second_col, first_col, second_col,\]\)\.transpose\(\)\n    divisor_df = pd\.DataFrame\(index=report_w_cs\.index, data=data, columns=report_w_cs\.columns\)\n\n    ## Compute percentages actual and cumulative\n    report_percentage = np\.round\(report_w_cs\.divide\(divisor_df, axis=1\) \* 100, 2\)",
    r"""    ## Compute percentages actual and cumulative using broadcasting
    divisor_series = pd.Series([first_col_total, second_col_total, first_col_total, second_col_total], index=report_w_cs.columns)
    report_percentage = np.round(report_w_cs.divide(divisor_series, axis=1) * 100, 2)""",
    content,
    flags=re.MULTILINE
)

with open(file_path, "w") as f:
    f.write(new_content)
