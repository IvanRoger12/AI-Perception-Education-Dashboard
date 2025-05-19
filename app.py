
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI & Education Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Impact on Statistics Students in Ankara")

@st.cache_data
def load_data():
    return pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
universities = st.sidebar.multiselect("Select University", df["University"].unique(), default=df["University"].unique())
genders = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())

filtered_df = df[df["University"].isin(universities) & df["Gender"].isin(genders)]

st.subheader("🎓 Filtered Data")
st.dataframe(filtered_df)

# Bar Chart: AI Knowledge Level
df_ai_knowledge = filtered_df["AI and Automation Knowledge Level"].value_counts().reset_index()
df_ai_knowledge.columns = ["Knowledge Level", "Count"]

fig3 = px.bar(
    df_ai_knowledge,
    x="Knowledge Level",
    y="Count",
    title="AI Knowledge Levels",
    color="Knowledge Level",
    color_discrete_sequence=px.colors.sequential.Blues
)

fig3.update_traces(marker_line_color='white', marker_line_width=1.5)
fig3.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Poppins", size=14, color="#1E3A8A"),
    hovermode="x unified"
)

st.plotly_chart(fig3, use_container_width=True)
