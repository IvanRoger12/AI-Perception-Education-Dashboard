
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="AI & Statistics Dashboard", layout="wide", page_icon="📊")

@st.cache_data
def load_data():
    df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")
    gpa_map = {
        '2.00 or below': 1.75, '2.01 - 2.50': 2.25, 
        '2.51 - 3.00': 2.75, '3.01 - 3.50': 3.25, 
        '3.51 - 4.00': 3.75
    }
    knowledge_map = {'No knowledge': 0, 'Little knowledge': 1, 'Moderate knowledge': 2, 'High knowledge': 3}
    df["GPA_Numeric"] = df["GPA"].map(gpa_map)
    df["AI_Knowledge_Score"] = df["AI and Automation Knowledge Level"].map(knowledge_map)
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
universities = st.sidebar.multiselect("Select Universities", df["University"].unique(), default=df["University"].unique())
gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())

filtered_df = df[df["University"].isin(universities) & df["Gender"].isin(gender)]

# Display stats
st.title("📊 AI & Statistics Education Dashboard")
st.markdown("An interactive exploration of students' perspectives on AI and their academic paths.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(filtered_df))
col2.metric("Average GPA", round(filtered_df["GPA_Numeric"].mean(), 2))
col3.metric("Avg. AI Knowledge", round(filtered_df["AI_Knowledge_Score"].mean(), 2))

st.divider()

# Graph 1: AI Knowledge Levels
fig1 = px.bar(
    filtered_df["AI and Automation Knowledge Level"].value_counts().reset_index(),
    x="index",
    y="AI and Automation Knowledge Level",
    labels={"index": "Knowledge Level", "AI and Automation Knowledge Level": "Count"},
    title="AI Knowledge Levels"
)
st.plotly_chart(fig1, use_container_width=True)

# Graph 2: Gender Distribution
fig2 = px.pie(filtered_df, names="Gender", title="Gender Distribution")
st.plotly_chart(fig2, use_container_width=True)

# Graph 3: GPA Distribution
fig3 = px.histogram(filtered_df, x="GPA_Numeric", nbins=10, title="GPA Distribution")
st.plotly_chart(fig3, use_container_width=True)

# Graph 4: Clustering (GPA vs Age)
st.subheader("🧠 Clustering Students (GPA vs Age)")
if "GPA_Numeric" in filtered_df.columns and "Age" in filtered_df.columns:
    clustering_data = filtered_df.dropna(subset=["GPA_Numeric", "Age"])
    if len(clustering_data) >= 3:
        model = KMeans(n_clusters=3, random_state=42)
        clustering_data["Cluster"] = model.fit_predict(clustering_data[["GPA_Numeric", "Age"]])
        fig4 = px.scatter(clustering_data, x="GPA_Numeric", y="Age", color=clustering_data["Cluster"].astype(str), title="Clustering Students by GPA and Age")
        st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("""
---
<div style='text-align:center; font-size:0.9rem; color:#888;'>
    Built with ❤️ by <strong>Ivan Nfinda</strong><br>
    📍 Ankara, 2025 – All Rights Reserved.
</div>
""", unsafe_allow_html=True)
