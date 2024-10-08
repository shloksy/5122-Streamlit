import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment - Shlok Yeolekar")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)

# Removed non grouped bar graph because it was redundant and not a good visualization

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

#### My edits ####
st.write("## My additions")
# 1
sel_cat = st.selectbox("Select a category:", ("Furniture","Office Supplies","Technology"))

# 2
subcat_options = None
match sel_cat:
    case "Furniture":
        subcat_options = ["Bookcases", "Chairs", "Tables", "Furnishings"]
    case "Office Supplies":
        subcat_options = ["Labels", "Storage", "Art", "Binders", "Appliances", "Paper", "Envelopes", "Fasteners", "Supplies"]
    case "Technology":
        subcat_options = ["Phones", "Accessories", "Machines", "Copiers"]

sel_subcat = st.multiselect(f"Select a subcategory from {sel_cat}:", subcat_options)

# 3
if sel_subcat:
    filt_df = df[df['Sub_Category'].isin(sel_subcat)]
    sales_by_month = filt_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month, y="Sales")
else: 
    st.write(":red[Please select a subcategory to see charts.]")

# 4 & 5
try:
    total_sales = filt_df['Sales'].sum()
    total_profit = filt_df['Profit'].sum()
    overall_profit_margin = (total_profit/total_sales) * 100 if total_sales > 0 else 0

    total_sales_all = df['Sales'].sum()
    total_profit_all = df['Profit'].sum()
    overall_profit_margin_all = (total_profit_all / total_sales_all) * 100 if total_sales_all > 0 else 0

    opm_delta = overall_profit_margin - overall_profit_margin_all
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{opm_delta:.2f}%")
except Exception:
    st.write()
