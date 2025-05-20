
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎓 Education Dashboard - Ivan Nfinda", layout="wide")

# Custom CSS
def add_custom_css():
    st.markdown("""
    <style>
        body, html {
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background-color: #f9fafb;
        }
        h1 {
            background: -webkit-linear-gradient(#1E3A8A, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")
    df["GPA_Numeric"] = df["GPA"].map({
        "2.00 or below": 1.75,
        "2.01 - 2.50": 2.25,
        "2.51 - 3.00": 2.75,
        "3.01 - 3.50": 3.25,
        "3.51 - 4.00": 3.75
    })
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🎛️ Filters")
univ = st.sidebar.multiselect("University", df["University"].unique(), default=df["University"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
year = st.sidebar.multiselect("Year of Study", df["Year of Study"].unique(), default=df["Year of Study"].unique())

filtered_df = df[
    df["University"].isin(univ) &
    df["Gender"].isin(gender) &
    df["Year of Study"].isin(year)
]

# Header
st.title("📊 Comprehensive Student Analysis in Ankara")
st.markdown("**Dive into student data and uncover insights!**")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍🎓 Total Students", len(filtered_df))
col2.metric("🏫 Universities", filtered_df["University"].nunique())
col3.metric("🎯 Average GPA", round(filtered_df["GPA_Numeric"].mean(), 2) if not filtered_df.empty else 0)
col4.metric("🤖 AI Knowledge", filtered_df["AI and Automation Knowledge Level"].mode()[0] if not filtered_df.empty else "N/A")

# Charts
st.subheader("📌 Demographic Distribution")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(filtered_df, names="Gender", title="Gender")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(filtered_df, x="Year of Study", color="University", title="Years of Study by University")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📚 GPA and AI Knowledge")
col1, col2 = st.columns(2)

with col1:
    fig3 = px.box(filtered_df, x="University", y="GPA_Numeric", title="GPA Distribution by University")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.histogram(filtered_df, x="AI and Automation Knowledge Level", color="Gender", title="AI Knowledge by Gender")
    st.plotly_chart(fig4, use_container_width=True)

# Data table
st.subheader("🔍 Raw Data")
st.dataframe(filtered_df)

st.markdown("---")
st.markdown("💡 **Built with love by Ivan Nfinda | Last updated: May 2025**", unsafe_allow_html=True)
