
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Statistics & AI Perceptions in Ankara",
    page_icon="📊",
    layout="wide"
)

# Main Title
st.title("📊 Statistics Students & Artificial Intelligence in Ankara")
st.markdown("""
Welcome to this interactive dashboard based on a survey conducted among statistics undergraduates in Ankara, Turkey.
Explore how students perceive Artificial Intelligence and how they believe it will affect their careers and education paths.
""")

st.markdown("---")

# Load data
df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")

# Sidebar filters
st.sidebar.header("🔍 Filter the Data")
universities = st.sidebar.multiselect("Select Universities:", df["University"].unique(), default=list(df["University"].unique()))
genders = st.sidebar.multiselect("Select Gender:", df["Gender"].unique(), default=list(df["Gender"].unique()))
years = st.sidebar.multiselect("Select Year of Study:", df["Year of Study"].unique(), default=list(df["Year of Study"].unique()))

# Filter the DataFrame
filtered_df = df.copy()
if universities:
    filtered_df = filtered_df[filtered_df["University"].isin(universities)]
if genders:
    filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]
if years:
    filtered_df = filtered_df[filtered_df["Year of Study"].isin(years)]

# Display total records
st.markdown(f"### 🎯 Total Responses: {len(filtered_df)}")

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Gender Distribution")
    fig_gender = px.pie(filtered_df, names="Gender", hole=0.4,
                        title="Proportion of Genders", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    st.subheader("🏫 University Distribution")
    uni_counts = filtered_df["University"].value_counts().reset_index()
    uni_counts.columns = ["University", "Count"]
    fig_uni = px.bar(uni_counts, x="University", y="Count",
                     labels={"University": "University", "Count": "Number of Students"},
                     title="Number of Students per University", color="Count",
                     color_continuous_scale="Viridis")
    st.plotly_chart(fig_uni, use_container_width=True)

# Knowledge level in AI
st.subheader("🤖 AI and Automation Knowledge Level")
fig_knowledge = px.histogram(filtered_df, x="AI and Automation Knowledge Level", color="Gender",
                             barmode="group", title="Knowledge Level by Gender",
                             color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig_knowledge, use_container_width=True)

# AI's impact on career plans
st.subheader("🎯 Impact of AI on Career Plans")
impact_counts = filtered_df["Impact of AI on Career Plans"].value_counts().reset_index()
impact_counts.columns = ["Impact", "Count"]
fig_impact = px.bar(impact_counts, x="Impact", y="Count",
                    labels={"Impact": "Career Impact", "Count": "Number of Responses"},
                    color="Impact", title="Perceived Career Impact from AI",
                    color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_impact, use_container_width=True)

# Satisfaction with studying statistics
st.subheader("📚 Satisfaction with Studying Statistics")
fig_satisfaction = px.pie(filtered_df, names="Satisfaction with Studying Statistics",
                          title="Satisfaction Levels", hole=0.5,
                          color_discrete_sequence=px.colors.sequential.Teal)
st.plotly_chart(fig_satisfaction, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
💡 *Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/)*  
📌 Developed by [Your Name] – share your thoughts and feedback!  
🚀 Ready for the data-driven future.
""")
