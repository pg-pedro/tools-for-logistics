import streamlit as st

def welcome_page():
    text = """
    ## Welcome!

    ### What is this tool for?

    This web tool is designed to help logistics engineers create outbound reports efficiently. 

    It provides a user-friendly interface to upload data, preprocess and merge datasets, and generate various reports and dashboards. 
    
    The tool streamlines the process of data analysis, allowing users to focus on insights rather than repetitive tasks.

    #### Key Features:
    1. **Upload Data**: Supports CSV, XLS, and XLSX file formats up to 2GB.
    2. **Merge and Preprocess**: Convert data types, drop unnecessary columns, and set datetime indexes.
    3. **Select Report**: Choose from various report types tailored for logistics analysis.
    4. **Set Parameters and Create Dashboards**: Customize report parameters and generate interactive dashboards.
    5. **Download Report Data**: Export the processed data and reports for further analysis or sharing.

    ### Goal

    Relieve logistics engineers from running redundant analysis.
    
    ### Current Status

    Prototype.
    Test how the tool works and learn from it.
    """
    st.markdown(text)