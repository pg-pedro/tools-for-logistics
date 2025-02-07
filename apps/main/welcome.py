import streamlit as st

def welcome_page():
    text = """
    ## Welcome!

    ### What is this tool for?

    Web tool that creates logistics outbound reports. 
    Upload the required data to the tool, select a report you want to have and the tool will create it for you.

    1. Upload data
    2. Merge and Preprocess dataset(s)
    2. Select report
    3. Set parameters and create dashboards
    4. Download report data

    ### Goal

    Relieve logistics engineers from running redundant analysis.
    
    ### Current Status

    Prototype.
    Test how the tool works and learn from it.
    """
    st.markdown(text)