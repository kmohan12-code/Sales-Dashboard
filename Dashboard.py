import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import os
import warnings

warnings.filterwarnings("ignore")

# Streamlit Page Configuration
st.set_page_config(page_title="Superstore EDA", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# File Uploader
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])

# Load Data Function with Caching
@st.cache_data
def load_data(file):
    try:
        if file is not None:
            filename = file.name
            st.write(f"**Uploaded file:** {filename}")
            if filename.endswith((".csv", ".txt")):
                df = pd.read_csv(file, encoding="ISO-8859-1")
            elif filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(file)
            else:
                st.error("Unsupported file format!")
                return None
        else:
            os.chdir(r"C:\\Games\\st")  # Change this to your actual path
            default_file = "Superstore.csv"
            if default_file.endswith((".csv", ".txt")):
                df = pd.read_csv(default_file, encoding="ISO-8859-1")
            else:
                df = pd.read_excel(default_file)
        
        df.columns = df.columns.str.strip()
        if "Order Date" not in df.columns:
            st.error("Error: 'Order Date' column not found in dataset!")
            return None
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df = df.dropna(subset=["Order Date"])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load Data
df = load_data(fl)
if df is None:
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter by Date")
startDate, endDate = df["Order Date"].min(), df["Order Date"].max()
date1, date2 = st.sidebar.date_input("Start Date", startDate), st.sidebar.date_input("End Date", endDate)
date1, date2 = pd.to_datetime(date1), pd.to_datetime(date2)
if date1 > date2:
    st.error("Start Date cannot be after End Date!")
    st.stop()

df_filtered = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

region = st.sidebar.multiselect("Pick your Region", df_filtered["Region"].unique())
if region:
    df_filtered = df_filtered[df_filtered["Region"].isin(region)]

state = st.sidebar.multiselect("Pick the State", df_filtered["State"].unique())
if state:
    df_filtered = df_filtered[df_filtered["State"].isin(state)]

city = st.sidebar.multiselect("Pick the City", df_filtered["City"].unique())
if city:
    df_filtered = df_filtered[df_filtered["City"].isin(city)]

# Category-wise Sales
category_df = df_filtered.groupby(by=["Category"], as_index=False)["Sales"].sum()
layout = go.Layout(title=dict(text='My Graph', font=dict(size=20)))

col1, col2 = st.columns((2))
with col1:
    st.subheader("Category-wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales",
                 text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template="seaborn")
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Region-wise Sales")
    fig = px.pie(df_filtered, values="Sales", names="Region", hole=0.5)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(df_filtered, path=["Region", "Category", "Sub-Category"], values="Sales",
                  hover_data=["Sales"], color="Sub-Category")
fig3.update_layout(layout)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Relationship between Sales and Profits using Scatter Plot")
data1 = px.scatter(df_filtered, x="Sales", y="Profit", size="Quantity")
data1.update_layout(layout)
st.plotly_chart(data1, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment-wise Sales')
    fig = px.pie(df_filtered, values="Sales", names="Segment", template="plotly_dark")
    fig.update_traces(text=df_filtered["Segment"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader('Category-wise Sales')
    fig = px.pie(df_filtered, values="Sales", names="Category", template="gridon")
    fig.update_traces(text=df_filtered["Category"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

st.subheader(":point_right: Month-wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df.iloc[:5, [df.columns.get_loc(c) for c in ["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)
    
    df_filtered["month"] = df_filtered["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data=df_filtered, values="Sales", index=["Sub-Category"], columns="month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

with st.expander("View Data"):
    st.write(df_filtered.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))