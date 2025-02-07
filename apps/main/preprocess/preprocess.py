import pandas as pd
import streamlit as st

from apps.main.upload import file_manager as fm
from apps.widgets import dtframe

"""
List of global variables
 - df: pd.DataFrame
 - preview_container: st.empty
 - dtype_container: st.empty
"""

def page_intro():
    st.markdown('## Data Preprocessing')
    with st.expander('More Info'):
        text = """
        Prepare your data for analysis by converting data types, dropping unnecessary columns, and setting the Pandas index. 
        
        These steps ensure that your data is clean and ready for use in our analytical tools.
        """
        st.markdown(text)

def no_dataframe_yet():
    text = """
    #### No Dataframe yet!

    Please upload your data first.
    """
    st.markdown(text)


def dataframe_info():
    global file_name, df
    file_name, df = dtframe.select_dataframe('Dataframe To Preprocess')
    st.info(f'{file_name} selected')
    # Create container for later updates
    global preview_container 
    preview_container = st.empty()
    preview_container.dataframe(df.iloc[:300])
    st.markdown('---')

def get_dataframe_datatypes():
    dtypes = df.dtypes
    dtypes.name = 'Data Type'
    return dtypes

def update_dataframe_table():
    preview_container.dataframe(df.iloc[:300])

def update_dtype_table():
    dtypes = get_dataframe_datatypes()
    dtype_container.table(dtypes.astype(str))

def drop_columns():
    st.markdown('##### Remove columns by specifying label names.')
    label = 'Select Column(s) To Drop'
    options = df.columns
    cols_to_drop = st.multiselect(label, options)
    st.warning('This operation cannot be undone!')
    if st.button('Remove Col(s)'):
        with st.spinner('Removing Selected Column(s)'):
            df.drop(columns=cols_to_drop, inplace=True)
        st.success('Done!')
        update_dataframe_table()
        update_dtype_table()


def to_datetime_simple():
    """
    Displays an expandable section with brief explanation about the function and 
    a user interface for selecting options for pandas' to_datetime() method.
    
    Returns:
        - dict: A dictionary containing the selected options for the to_datetime() method. 
        
    """
    with st.expander('More Info'):
        text = """
        Brief Explanation Here
        """
        st.markdown(text)
    # Set pd.to_datetime parameters
    params = dict()
    dayfirst_tip = """
    **dayfirst : bool, default False**

    If True, parses dates with the day first, e.g. **"10/11/12"** is parsed as **2012-11-10**.
    """
    dayfirst = st.selectbox('Dayfirst', [True, False], index=1, help=dayfirst_tip)
    yearfirst_tip = """
    **yearfirst : bool, default False**

    - If True parses dates with the year first, e.g. "10/11/12" is parsed as 2010-11-12.

    - If both dayfirst and yearfirst are True, yearfirst is preceded (same as dateutil).
    """
    yearfirst = st.selectbox('Yearfirst', [True, False], index=1, help=yearfirst_tip)

    params['dayfirst'] = dayfirst
    params['yearfirst'] = yearfirst
    return params


def to_datetime_advanced():
    """
    Displays an expandable section with brief explanation about the datetime format and 
    a user interface for selecting advanced option for pandas' to_datetime() method.
    
    Returns:
        - dict: A dictionary containing the selected options for the to_datetime() method. 
        
    """
    with st.expander('More Info'):
        text = """
        Brief explanation on datetime format
        """
        st.markdown(text)
    params = dict()
    format_tip = """
    **format : str, default None**

    The strftime to parse time, e.g. "%d/%m/%Y". Note that "%f" will parse all the way up to nanoseconds. See strftime documentation for more information on choices.
    """
    placeholder = 'E.g.: %d/%m/%Y'
    format_dt = st.text_input('Specify date-time format', placeholder=placeholder, help=format_tip)
    params['format'] = format_dt
    return params

def convert_to_datetime(col_to_convert):
    """
    A function that provides a user interface to convert a column in a dataframe to a datetime format 
    using either a simple or advanced conversion method. 
    Simple method allows user to select options for dayfirst and yearfirst. 
    Advanced method allows user to select a custom format for datetime conversion. 
    When the user clicks the "Convert to Datetime" button, the selected column will be converted and 
    the dataframe and data type table will be updated accordingly.
    Parameters:
        - col_to_convert (str): The column name that the user wants to convert to datetime format.
    Returns:
        - None
    """
    st.markdown('###### Set Parameters')
    label = 'Select How To Transform To Datetime:'
    options = ['Simple', 'Advanced']
    conversion_mode = st.radio(label, options)
    if conversion_mode == 'Simple':
        params = to_datetime_simple()
    elif conversion_mode == 'Advanced':
        params = to_datetime_advanced()
    if st.button('Convert To Datetime'):
        with st.spinner(f'Converting {col_to_convert} to datetime...'):
            df[col_to_convert] = pd.to_datetime(df[col_to_convert], **params)
        st.success(f'Done! {col_to_convert} successfully converted!')
        update_dtype_table()
        update_dataframe_table()



def convert_to_string(col_to_convert: str):
    if st.button('Convert To String'):
        with st.spinner(f'Converting {col_to_convert} to string...'):
            df[col_to_convert] = df[col_to_convert].astype(str)
        st.success(f'Done! \n{col_to_convert} successfully converted!')
    update_dataframe_table()
    update_dtype_table()


def convert_to_integer(col_to_convert: str):
    if st.button('Convert To Int'):
        with st.spinner(f'Converting {col_to_convert} to integer...'):
            df[col_to_convert] = df[col_to_convert].astype(int)
        st.success(f'Done! \n{col_to_convert} successfully converted!')
    update_dataframe_table()
    update_dtype_table()

def convert_to_float(col_to_convert: str):
    if st.button('Convert To Float'):
        with st.spinner(f'Converting {col_to_convert} to float...'):
            df[col_to_convert] = df[col_to_convert].astype(float)
        st.success(f'Done! \n{col_to_convert} successfully converted!')
    update_dataframe_table()
    update_dtype_table()

def _get_exact_datatype(dataframe: pd.DataFrame, column_name: str):
    """
    Returns the first non-NA value and its datatype for a given column in a dataframe.
    If all values in the given column are NA, the function will return None.

    Parameters:
        - dataframe (pd.DataFrame): The input dataframe.
        - column_name (str): The column name for which the first non-NA value and its datatype will be returned.

    Returns:
        - tuple: A tuple of the form (value, value_type) where value is the first non-NA value
                 and value_type is the datatype of that value as string.

    Example:
    df = pd.DataFrame({'A':[1, 2, np.nan], 'B':['a', 'b', 'c']})
    _get_exact_datatype(df, 'A')
    # Returns (1, <class 'numpy.float64'>)
    """
    mask = ~dataframe[column_name].isna()
    value = dataframe.loc[mask, column_name].iloc[0]
    value_type = str(type(value)) 
    return value, value_type

def datatype_conversion():
    st.markdown('##### Convert a column')
    with st.expander('More Info'):
        text = """
        Sometimes you will need to change the type of the data. 
        This may be due to formats that do not include type information.

        Three type of conversion are supported:
        - Object (string) -> Datetime
        - Integer/Float to String
        - Float to Integer
        """
        st.markdown(text)

    # Diplay datatypes
    dtypes = get_dataframe_datatypes()
    global dtype_container
    dtype_container = st.empty()
    dtype_container.table(dtypes.astype(str))

    # Select column to convert
    label = 'Select Column(s) To Convert'
    options = df.columns
    col_to_convert = st.selectbox(label, options)

    # Select what to convert to
    label = 'Select Data Type To Convert To'
    options = ['Integer', 'Float', 'String', 'Datetime']
    convert_to_type = st.selectbox(label, options)
    # Conversion recap
    data_type = dtypes.loc[col_to_convert]
    sample_datatype, exact_data_type = _get_exact_datatype(df, col_to_convert)
    recap = f"""
    The column **{col_to_convert}** currently **{data_type} - {exact_data_type} - {sample_datatype}** will be converted to **{convert_to_type}**
    """
    st.warning(recap)

    # Data-type conversion section
    if convert_to_type == 'Integer':
        convert_to_integer(col_to_convert)
    elif convert_to_type == 'Float':
        convert_to_float(col_to_convert)
    elif convert_to_type == 'String':
        convert_to_string(col_to_convert)
    elif convert_to_type == 'Datetime':
        convert_to_datetime(col_to_convert)

def _remove_row_index_column():
    if 'index' in df.columns:
        df.drop(columns=['index'], inplace=True)

def set_index():
    st.markdown('##### Set Index')
    with st.expander('More Info'):
        text = """
        It sets a column into the index. 
        The dataframe will be sorted afterwards.
        """
        st.markdown(text)

    # Select column to set as index
    label = 'Select Column To Set As Index'
    options = df.columns
    new_index = st.selectbox(label, options)
    # Set index
    if st.button('Set Index'):
        with st.spinner(f'Setting {new_index} as new index...'):
            # Reset current index first to avoid losing that column
            df.reset_index(inplace=True)
            df.set_index(new_index, inplace=True)
            df.sort_index(inplace=True)
            _remove_row_index_column()
        st.success('Done!')
        update_dataframe_table()
        update_dtype_table()

def reset_index():
    st.markdown('##### Reset Index')
    with st.expander('More Info'):
        text = """
        It resets the index of the DataFrame, and uses the default one instead.
        """
        st.markdown(text)
    if st.button('Reset Index'):
        with st.spinner('Resetting Index...'):
            df.reset_index(inplace=True)
        st.success('Done!')
        update_dataframe_table()
        update_dtype_table()

def download_section():
    st.markdown('##### Download Dataframe To Csv')
    if st.button('Prepare File'):
        with st.spinner('Preparing Data For Download...'):
            csv = fm.dataframe_to_csv(df)
        st.success('Done!')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f'{file_name}.csv',
            mime='text/csv',
        )


def custom_preprocessing():
    st.markdown('### Dataframe Operations')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            'Convert Datatype', 
            'Drop Column(s)', 
            'Set Index', 
            'Reset Index',
            'Download'
        ]
    )

    with tab1:
        datatype_conversion()

    with tab2:
        drop_columns()

    with tab3:
        set_index()

    with tab4:
        reset_index()

    with tab5:
        download_section()
    

def run_page():
    page_intro()
    if fm.are_there_dataframes():
        dataframe_info()
        custom_preprocessing()
    else:
        no_dataframe_yet()

def preprocess_page():
    run_page()