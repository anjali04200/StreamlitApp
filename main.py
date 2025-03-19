import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport

# Function to improve layout
def set_page_config():
    st.set_page_config(
        page_title="Exploratory Data Analysis with YData Profiling",
        page_icon=":bar_chart:",
        layout="wide"
    )

# Apply custom page configuration
set_page_config()

# Add some custom styling
st.markdown("""
    <style>
        .reportview-container {
            background-color: #f1f1f1;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            transition: none;
            border : 2px solid #388E3C;
        }
        .stButton>button:hover {
            background-color: #4CAF50;  
            color: white;
            transition: none; 
            border : 2px solid #006400;
        }
        .stFileUploader>label {
            font-size: 18px;
        }
        .stHeader>h1 {
            font-size: 36px;
            color: #4CAF50;
        }
        .stText {
            font-size: 18px;
            color: #333;
        }
        .stMarkdown {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and dataset upload instructions
st.sidebar.title("Exploratory Data Analysis")
st.sidebar.write(
    "Upload a CSV or JSON file to generate an exploratory data analysis report. "
    "Alternatively, use the sample dataset to explore the functionality."
)

uploaded_file = st.sidebar.file_uploader("Choose a file (CSV/JSON)", type=["csv", "json"])

# Function to display instructions
def display_instructions():
    st.markdown("""
    # Welcome to the Exploratory Data Analysis (EDA) App!
    
    This application generates a **Pandas Profiling** report using `ydata-profiling` for any dataset you upload.
    - Upload your own dataset via the file uploader on the left.
    - If you prefer, click the button below to use a sample dataset.
    - After uploading, a comprehensive **Exploratory Data Analysis** report will be generated for you.

    **Features :**
    - Automatically detects columns and their types.
    - Visualizes distributions, correlations, and more.
    - Shows missing values, outliers, and duplicate records.
    """, unsafe_allow_html=True)

# Function to load the dataset
def load_data(uploaded_file):
    if uploaded_file is not None:
        # Check the file type and load accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            return pd.read_csv(uploaded_file)
        elif file_extension == 'json':
            return pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file format! Please upload a CSV or JSON file.")
            return None
    else:
        return None

# Display instructions when no file is uploaded
if uploaded_file is None:
    display_instructions()
    st.sidebar.write("Use the button below to generate a sample dataset.")
    if st.sidebar.button('Generate Sample Dataset'):
        # Generate random data for the sample dataset
        @st.cache_data
        def load_sample_data():
            return pd.DataFrame(np.random.rand(100, 5), columns=['a', 'b', 'c', 'd', 'e'])

        df = load_sample_data()
        st.write("### Sample DataFrame :")
        st.write(df)
        pr = ProfileReport(df, explorative=True)
        st.write("### Exploratory Data Analysis Report :")
        st.components.v1.html(pr.to_html(), height=800)

else:
    # If a file is uploaded, load the data and display the dataframe
    df = load_data(uploaded_file)

    if df is not None:
        # Show the input DataFrame
        st.header('**Uploaded DataFrame**')
        st.write(df.head())  # Show only first few rows for preview

        # Display progress bar while loading the profiling report
        with st.spinner('Generating EDA report...'):
            pr = ProfileReport(df, explorative=True)

        # Display the profiling report
        st.header('**Pandas Profiling Report**')
        st.components.v1.html(pr.to_html(), height=5000)  #is used in Streamlit to embed an HTML representation of the pr object (which is likely a ProfileReport from the ydata-profiling library) directly into your Streamlit app.

# Add some user-friendly error handling and logging
def display_error(message):
    st.error(message)

# Display error if something goes wrong
try:
    # Try the main logic here
    pass
except Exception as e:
    display_error(f"An error occurred: {e}")
