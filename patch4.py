import re

file_path = "apps/main/upload/file_manager.py"
with open(file_path, "r") as f:
    content = f.read()

# Make pd.concat more efficient by accumulating dataframes in a list and then concatenating once
new_content = re.sub(
    r"    df = pd\.DataFrame\(\)\n    for i, sheet_name in enumerate\(selected_sheets, 1\):\n        with st\.spinner\(f'Reading \{sheet_name\}'\):\n            tmp_df = _file\.parse\(sheet_name, \*\*params\)\n            df = pd\.concat\(\[df, tmp_df\], ignore_index=True\)",
    r"""    df_list = []
    for i, sheet_name in enumerate(selected_sheets, 1):
        with st.spinner(f'Reading {sheet_name}'):
            tmp_df = _file.parse(sheet_name, **params)
            df_list.append(tmp_df)
    df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()""",
    content,
    flags=re.MULTILINE
)

with open(file_path, "w") as f:
    f.write(new_content)
