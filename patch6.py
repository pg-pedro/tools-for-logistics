import re

file_path = "apps/outbound/abc_classification/report_generator.py"
with open(file_path, "r") as f:
    content = f.read()

# Use broadcasting for divide instead of list
new_content = re.sub(
    r"    # Compute totals\n    total_sku = pt\.shape\[0\]\n    total_picklines = pt\[ORDERLINES\]\.sum\(\)\n\n    # Compute percentages\n    pt_final = pt_cumsum\.divide\(\[total_sku, total_picklines\]\)\n    pt_final = round\(pt_final \* 100, 2\)",
    r"""    # Compute totals
    total_sku = pt.shape[0]
    total_picklines = pt[ORDERLINES].sum()

    # Compute percentages using broadcasting
    divisor_series = pd.Series([total_sku, total_picklines], index=[SKU_PER, ORDERLINES])
    pt_final = pt_cumsum.divide(divisor_series, axis=1)
    pt_final = round(pt_final * 100, 2)""",
    content,
    flags=re.MULTILINE
)

new_content = re.sub(
    r"    # Compute totals\n    total_sku = pt\.shape\[0\]\n    total_quantity = pt\[QTY\]\.sum\(\)\n\n    # Compute percentages\n    pt_final = pt_cumsum\.divide\(\[total_sku, total_quantity\]\)\n    pt_final = round\(pt_final \* 100, 2\)",
    r"""    # Compute totals
    total_sku = pt.shape[0]
    total_quantity = pt[QTY].sum()

    # Compute percentages using broadcasting
    divisor_series = pd.Series([total_sku, total_quantity], index=[SKU_PER, QTY])
    pt_final = pt_cumsum.divide(divisor_series, axis=1)
    pt_final = round(pt_final * 100, 2)""",
    new_content,
    flags=re.MULTILINE
)

with open(file_path, "w") as f:
    f.write(new_content)
