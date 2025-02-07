from collections import namedtuple

import streamlit as st
import pandas as pd

import apps.main.upload.file_manager as fm
from .settings import *

DISPLAY_DATAFRAME = dict()
DisplayData = namedtuple('DisplayData', ['name', 'location'])

def page_intro():
    st.markdown('## Upload Your File Here')
    with st.expander('More Info'):
        text = """
        Upload a file using this section.

        Limitations:
        - Max file size: 2Gb.
        - File format  : .csv, .xls, .xlsx
        """
        st.markdown(text)

def upload_multiple_files():
    label = 'Choose a file'
    filetype = ['csv', 'xls', 'xlsx']
    help_tip = """
    Currently .csv, .xls and .xlsx files are supported.
    Parquet format will be soon available.

    For faster upload / read operations, opt for .csv files.
    """
    uploaded_files = st.file_uploader(
                            label, 
                            type=filetype, 
                            help=help_tip, 
                            accept_multiple_files=True
                            )
    
    # Save files to session state
    fm.save_files_to_session_state(uploaded_files)
    st.markdown('---')


def show_uploaded_files():
    """It shows an overview of all uploaded files. 
    While it is capable of handling multiple files, currently only a single file upload is supported.

    The function first checks whether any files have been uploaded and if so, it displays them using Markdown. 
    It also checks the file extension of each uploaded file and calls the appropriate file preparation function (prepare_excel_file for Excel files, and prepare_csv_file for CSV files) to make sure they can be displayed properly.

    If no files have been uploaded yet, the function displays a message indicating that no files have been uploaded and prompts the user to upload some data.

    """
    visible = fm.are_there_uploaded_files()
    if visible:
        st.markdown('### Uploaded File(s)')
        # Loop through uploaded files and set import parameters
        for i, file_name in enumerate(fm.session_uploaded_keys(), 1):
            is_excel = file_name.lower().endswith(('.xlsx', '.xls'))
            is_csv = file_name.lower().endswith('.csv')
            st.markdown(f'#### {i}. {file_name}')
            if is_excel:
                fm.prepare_excel_file(file_name)
            elif is_csv:
                fm.prepare_csv_file(file_name)
    else:
        st.markdown('**No File Yet.** Please Upload Some Data.')

def select_files_to_process():
    """It displays a user interface that allows the user to select which uploaded files they want to process.
    Returns:
        - None
    """
    st.markdown('#### Select Files To Process')
    for i, file_name in enumerate(fm.session_uploaded_keys(), 1):
        process_file = st.checkbox(label=file_name, value=True, key=f'{file_name}_chkbx')
        st.session_state[PROCESS_FILE][file_name] = process_file


def process_to_dataframe_section() -> None:
    """
    Displays a user interface that allows the user to process previously uploaded files into pandas dataframes. The user can specify the CSV column separator if needed. This function also displays a preview of the dataframe after processing.
    Returns:
        - None
    """
    visible = fm.are_there_uploaded_files()
    if visible:
        st.markdown('### Process To Dataframe')
        with st.expander('More Info'):
            text = """
            Uploaded file needs transforming into [pandas dataframes](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).
            
            Pandas is a powerful library that allows for easy manipulation and analysis of data. 
            This transformation process is an important step in creating effective dashboards and reports.

            It is important to note that when uploading a CSV file, a separator must be specified in order to properly process the data. 
            This separator is used to distinguish between the different data fields within the file. 
            Without specifying a separator, the data may not be properly processed and may not be useful for creating dashboards and reports.

            Please press _Process Data_ to create Pandas dataframe(s).
            """
            st.markdown(text)
        
        select_files_to_process()
        process_button =  st.button('Process Selected', type='primary')
        st.markdown('---')

        for i, file_name in enumerate(fm.session_uploaded_keys(), 1):
            # Set Dataframe Preview empty containers
            dataframe_info = st.empty()
            dataframe_container = st.empty()
            container = DisplayData(dataframe_info, dataframe_container)
            DISPLAY_DATAFRAME[file_name] = container
            if file_name in st.session_state[DATAFRAME].keys():
                dataframe = fm.get_dataframe(file_name)
                fm.display_dataframe(dataframe, f'{i}. {file_name}', DISPLAY_DATAFRAME[file_name])

        # if st.button('Process Selected', type='primary'):
        if process_button:

            for i, file_name in enumerate(fm.session_uploaded_keys(), 1):

                with st.spinner(f'Processing {file_name}...'):
                    # file type selector
                    is_excel = file_name.lower().endswith(('.xlsx', '.xls'))
                    is_csv = file_name.lower().endswith('.csv')
                    process_file = st.session_state[PROCESS_FILE][file_name]
                    # Select csv or excel read function
                    if is_excel and process_file:
                        _file = st.session_state[XL_FILE].get(file_name)
                        dataframe = fm.process_excel_file(file_name, _file)
                        st.success(f'{file_name} processed successfully.')
                    elif is_csv and process_file:
                        uploaded_file = fm.get_uploaded_file(file_name)
                        dataframe = fm.process_csv_file(file_name, uploaded_file)
                        st.success(f'{file_name} processed successfully.')
        
        for i, file_name in enumerate(fm.session_uploaded_keys(), 1):
            if file_name in fm.session_dataframe_keys():
                dataframe = fm.get_dataframe(file_name)
                fm.display_dataframe(dataframe, f'{i}. {file_name}', DISPLAY_DATAFRAME[file_name])
        


def upload_page():
    page_intro()
    upload_multiple_files()
    show_uploaded_files()
    process_to_dataframe_section()