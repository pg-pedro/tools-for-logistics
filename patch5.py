import re

file_path = "apps/outbound/general_profile/utils.py"
with open(file_path, "r") as f:
    content = f.read()

# Make add_dt_info vectorized using pandas dt accessor
new_content = re.sub(
    r"def add_dt_info\(dataframe: pd\.DataFrame\):\n    days = \[dt\.strftime\('%A'\) for dt in dataframe\.index\]\n    months = \[dt\.strftime\('%b'\) for dt in dataframe\.index\]\n    dataframe\[DAYS\] = days\n    dataframe\[MONTHS\] = months    ",
    r"""def add_dt_info(dataframe: pd.DataFrame):
    dataframe[DAYS] = dataframe.index.strftime('%A')
    dataframe[MONTHS] = dataframe.index.strftime('%b')""",
    content,
    flags=re.MULTILINE
)

with open(file_path, "w") as f:
    f.write(new_content)
