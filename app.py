# Import necessary packages
import datetime 
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go 
import streamlit as st 

# Set the page configuration
st.set_page_config(
    page_title="Market Dashboard Application",
    page_icon="📊",
    layout="wide",
)

# Set the background color using markdown
st.markdown(
    """
    <style>
    .stApp {
        background-color: #87CEEB;  /* Sky blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title for the Streamlit app
st.title("📊 Market Dashboard Application")

# Sidebar for user input
st.sidebar.header("User Input")

# Function to get user input from the sidebar
def get_input():
    symbol = st.sidebar.text_input("Enter Stock Symbol(Please use .NS extension for Indian stocks)", "INFY.NS").upper()
    
    # Get the current date
    today = datetime.date.today()
    
    # Allow user to select start and end dates with default values
    start_date = st.sidebar.date_input("Start Date (Click on the dates to change range)", today - datetime.timedelta(days=365))
    end_date = st.sidebar.date_input("End Date", today)

    # Ensure the start date is before the end date
    if start_date > end_date:
        st.sidebar.error("Error: End date must fall after the start date.")
    
    return symbol, start_date, end_date

# Function to fetch data from Yahoo Finance
@st.cache_data(show_spinner=False)
def get_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    if df.empty:
        st.warning(f"No data found for symbol: {symbol}")
    return df 

# Get user inputs
symbol, start_date, end_date = get_input()

# Fetch the data
df = get_data(symbol, start_date, end_date)

# If data is available, display the analysis
if not df.empty:
    # Display historical prices
    st.subheader(f"Historical Prices for {symbol}")
    st.dataframe(df)

    # Display data statistics
    st.subheader("Data Statistics")
    st.write(df.describe())

    # Display historical price chart - Adjusted Close Price
    st.subheader("Historical Price Chart - Adjusted Close Price")
    st.line_chart(df['Adj Close'])

    # Display trading volume
    st.subheader("Trading Volume Over Time")
    st.bar_chart(df['Volume'])

    # Display candlestick chart
    st.subheader("Candlestick Chart")
    fig = go.Figure(
        data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )]
    )
    st.plotly_chart(fig)
else:
    st.error("No data to display for the selected date range and symbol.")
