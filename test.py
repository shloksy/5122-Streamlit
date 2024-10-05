import streamlit as st
import pandas as pd
import numpy as np

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")

# Load the dataset and handle potential errors
try:
    df = pd.read_csv("Superstore_Sales_utf8.csv")
except Exception as e:
    st.error(f"Error loading the CSV file: {e}")
    st.stop()

# Print the column names for debugging
st.write("Column names:", df.columns.tolist())

# Ensure the necessary columns exist in the dataframe
required_columns = ['Category', 'Sub_Category', 'Sales', 'Profit', 'Order_Date']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"The following required columns are missing in the CSV file: {missing_columns}")
    st.stop()

# Parse the 'Order_Date' column if it exists
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

st.dataframe(df)

# Bar chart of sales by category
st.write("### Bar Chart of Sales by Category")
st.bar_chart(df.groupby("Category")["Sales"].sum())

# Aggregated bar chart of sales by category
st.write("### Aggregated Bar Chart of Sales by Category")
aggregated_df = df.groupby("Category", as_index=False).sum()
st.dataframe(aggregated_df)
st.bar_chart(aggregated_df, x="Category", y="Sales", color="#04f")

# Aggregated sales by month
df.set_index('Order_Date', inplace=True)
sales_by_month = df['Sales'].resample('M').sum()

st.write("### Sales by Month")
st.dataframe(sales_by_month)
st.line_chart(sales_by_month)

st.write("## Your additions")

# Categorized data
data = {
    'Category': ['Technology', 'Furniture', 'Office Supplies'],
    'Sub_Category': {
        'Technology': ['Phones', 'Appliances', 'Machines', 'Copiers'],
        'Furniture': ['Bookcases', 'Chairs', 'Tables', 'Storage', 'Furnishings'],
        'Office Supplies': [
            'Labels', 'Art', 'Binders', 'Paper', 'Accessories', 'Envelopes',
            'Fasteners', 'Supplies'
        ]
    }
}

# Step (1): Add a dropdown for Category
category = st.selectbox("Select a Category", data['Category'])

# Step (2): Add a multi-select for Sub_Category in the selected Category
if category:
    sub_categories = data['Sub_Category'][category]
    selected_sub_categories = st.multiselect(f"Select Sub-Categories in {category}", sub_categories)

# Display selected options
st.write(f"Selected Category: {category}")
st.write(f"Selected Sub-Categories: {selected_sub_categories}")

# Filter the dataframe based on selected category and sub-categories
if selected_sub_categories:
    filtered_df = df[(df['Category'] == category) & (df['Sub_Category'].isin(selected_sub_categories))]

    # Step (3): Show a line chart of sales for the selected items in (2)
    st.write("### Sales Line Chart")
    sales_chart = filtered_df.groupby('Order_Date')['Sales'].sum().reset_index()
    st.line_chart(sales_chart, x='Order_Date', y='Sales')

    # Calculate metrics
    total_sales = filtered_df['Sales'].sum()S
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = total_profit / total_sales * 100

    # Overall average profit margin for all products across all categories
    overall_avg_profit_margin = df['Profit'].sum() / df['Sales'].sum() * 100
    delta_profit_margin = overall_profit_margin - overall_avg_profit_margin

    # Step (4): Show three metrics
    st.write("### Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")

# Display selected options
st.write(f"Selected Category: {category}")
st.write(f"Selected Sub-Categories: {selected_sub_categories}")
