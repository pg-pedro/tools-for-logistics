import streamlit as st

CUSTOM_CSS = """
    <style>
    .custom-container {
        width: 800px !important;
        max-width: 1200px !important;
        margin: auto;
        padding: 20px;
    }
    </style>
    """

V1_CSS = """
    <style>
    .v1-container {
        width: 640px !important;
        max-width: 1200px !important;
        margin: auto;
        padding: 20px;
    }
    </style>
    """


def page_intro():

    st.markdown('## How To Use This Tool :thinking_face:')


def upload_data():
    st.markdown('### 1. Upload Data')
    
    st.components.v1.html(
        f"""
        <iframe src="https://scribehow.com/embed/How_to_Upload_CSV_Files__QuSECxdJRM-P8IK0Qs6AlA" width="100%" height="640" allowfullscreen frameborder="0"></iframe>
        """,
        height=680,
        scrolling=True,
    )
    st.markdown('---')


def preprocess_data():
    st.markdown('### 2. Set Datetime Index')
    
    st.components.v1.html(
        f"""
        <iframe src="https://scribehow.com/embed/Convert_Column_To_Datetime_And_Set_As_Index__dSLOyGEHStyhUPzpW_RL2A" width="100%" height="640" allowfullscreen frameborder="0"></iframe>
        """,
        height=680,
        scrolling=True,
    )
    st.markdown('---')

def abc_report():
    st.markdown('### 3. ABC Classification Report')
    
    st.components.v1.html(
        f"""
        <iframe src="https://scribehow.com/embed/Generate_ABC_Classification_Report__yk9HjwK_Ra2naDywdScJBw" width="100%" height="640" allowfullscreen frameborder="0"></iframe>
        """,
        height=680,
        scrolling=True,
    )
    st.markdown('---')


def run_page():
    page_intro()
    upload_data()
    preprocess_data()
    abc_report()


def how_to_page():
    run_page()
    st.markdown('WIP - Work in Progress :construction: :grin:')