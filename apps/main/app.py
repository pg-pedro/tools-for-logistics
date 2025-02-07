import streamlit as st
from streamlit_option_menu import option_menu
# https://github.com/victoryhb/streamlit-option-menu

# Main App Imports
from .welcome import welcome_page
from .upload import upload_page, data_storage_initialize
from .preprocess import preprocess_page

# Apps Imports
from apps.outbound import orderline_pattern_page
from apps.outbound import abc_classification_page
from apps.outbound import general_outbound_page
from apps.main.merge.merge import merge_page

# Side Menu Section
def page_config():
    st.set_page_config(
        page_title="Tools for Logistics",
        initial_sidebar_state="expanded",
    )

def main_menu():
    with st.sidebar:
        main_selection = option_menu(None, ['Home', 'Upload', 'Preprocess', 'Merge', 'Analytics - Outbound',], 
            icons=['house', 'cloud-upload', 'file-spreadsheet', 'journal-plus', 'box-arrow-up'], 
            menu_icon="cast", default_index=0, orientation="vertical",
            styles= {
            "nav-link-selected": {"background-color": "#002664"}
            }
        )
    return main_selection


def outbound_selection():
    label = 'Select Outbound Tool'
    options = ['Orderline Pattern', 'ABC Classification', 'Outbound Overview']
    options = ['---'] + sorted(options)
    selected_tool = st.sidebar.selectbox(label, options)
    if selected_tool == 'Orderline Pattern':
        orderline_pattern_page()
    elif selected_tool == 'ABC Classification':
        abc_classification_page()
    elif selected_tool == 'Outbound Overview':
        general_outbound_page()
    else:
        st.markdown('**Please select a tool from the dropdown menu on the left side**')

    return selected_tool


def main():
    """Main function to run the application. 
    It creates a sidebar with main menu options 'Home', 'Upload', 'Preprocess', 'Profiler', 'Tools'. 
    Based on the user selection, corresponding function is called.
    """
    st.sidebar.markdown('# Main Menu')
    main_selection = main_menu()
    if main_selection == 'Home':
        welcome_page()
    elif main_selection == 'Upload':
        upload_page()
    elif main_selection == 'Preprocess':
        preprocess_page()
    elif main_selection == 'Merge':
        merge_page()
    elif main_selection == 'Profiler':
        ...
    elif main_selection == 'Analytics - Outbound':
        outbound_selection()

    st.sidebar.caption('Brought to you by pg-pedro')

def run():
    """
    """
    page_config()
    data_storage_initialize()
    st.title('Tools for Logistics')
    main()