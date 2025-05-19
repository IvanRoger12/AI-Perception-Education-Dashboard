
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI & Students | Statistics Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")
    return df

st.markdown("## 🎓 AI & Statistics in Ankara")
st.markdown("Explore how AI impacts students' perceptions, career plans and academic paths.")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
universities = ["All"] + sorted(df["University"].dropna().unique().tolist())
selected_uni = st.sidebar.selectbox("University", universities)

genders = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", genders)

years = ["All"] + sorted(df["Year of Study"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Year of Study", years)

gpa_levels = ["All"] + sorted(df["GPA"].dropna().unique().tolist())
selected_gpa = st.sidebar.selectbox("GPA Range", gpa_levels)

# Filter logic
filtered_df = df.copy()
if selected_uni != "All":
    filtered_df = filtered_df[filtered_df["University"] == selected_uni]
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year of Study"] == selected_year]
if selected_gpa != "All":
    filtered_df = filtered_df[filtered_df["GPA"] == selected_gpa]

# KPI section
st.markdown("### 📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(filtered_df))
col2.metric("Average GPA", filtered_df["GPA"].mode()[0] if not filtered_df.empty else "N/A")
col3.metric("Universities", filtered_df["University"].nunique())

# Charts
st.markdown("### 🎯 Distribution")
col1, col2 = st.columns(2)
with col1:
    fig1 = px.pie(filtered_df, names="University", title="University Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(filtered_df, x="GPA", title="GPA Distribution", color="Gender")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 🤖 AI Awareness & Concerns")
col1, col2 = st.columns(2)
with col1:
    fig3 = px.bar(
        filtered_df["AI and Automation Knowledge Level"].value_counts().reset_index(),
        x="index", y="AI and Automation Knowledge Level",
        labels={"index": "Knowledge Level", "AI and Automation Knowledge Level": "Count"},
        title="AI Knowledge Levels"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.bar(
        filtered_df["Anxiety Level"].value_counts().reset_index(),
        x="index", y="Anxiety Level",
        labels={"index": "Anxiety Level", "Anxiety Level": "Count"},
        title="AI Anxiety Levels"
    )
    st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("""
<hr style='margin-top: 30px;'>
<div style='text-align:center; font-size: 0.85rem; color: gray;'>
Made with 💡 by <strong>Ivan Nfinda</strong> | Updated: May 2025
</div>
""", unsafe_allow_html=True)
