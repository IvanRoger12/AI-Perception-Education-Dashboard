
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="AI & Statistics Education Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")
    gpa_map = {
        "2.00 or below": 1.75, "2.01 - 2.50": 2.25,
        "2.51 - 3.00": 2.75, "3.01 - 3.50": 3.25, "3.51 - 4.00": 3.75
    }
    df["GPA_Numeric"] = df["GPA"].map(gpa_map)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_uni = st.sidebar.multiselect("University", df["University"].unique(), df["University"].unique())
selected_gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), df["Gender"].unique())

filtered_df = df[df["University"].isin(selected_uni) & df["Gender"].isin(selected_gender)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(filtered_df))
col2.metric("Avg GPA", round(filtered_df["GPA_Numeric"].mean(), 2) if not filtered_df.empty else "N/A")
col3.metric("Universities", filtered_df["University"].nunique())

# Plots
st.subheader("🎓 University Distribution")
if not filtered_df.empty:
    fig1 = px.histogram(filtered_df, x="University", color="University", title="Students per University")
    st.plotly_chart(fig1, use_container_width=True)

st.subheader("🤖 AI Knowledge Levels")
if "AI and Automation Knowledge Level" in filtered_df.columns:
    fig2 = px.bar(
        filtered_df["AI and Automation Knowledge Level"].value_counts().reset_index(),
        x="index", y="AI and Automation Knowledge Level",
        labels={"index": "Knowledge Level", "AI and Automation Knowledge Level": "Count"},
        title="AI Knowledge Levels"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Clustering with GPA and Age
st.subheader("🔍 Clustering: GPA vs Age")
if "Age" in filtered_df.columns and "GPA_Numeric" in filtered_df.columns and not filtered_df.empty:
    clustering_df = filtered_df[["Age", "GPA_Numeric"]].dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(clustering_df)

    kmeans = KMeans(n_clusters=3, n_init=10)
    clustering_df["Cluster"] = kmeans.fit_predict(scaled)

    final_df = filtered_df.copy()
    final_df["Cluster"] = clustering_df["Cluster"].values

    fig3 = px.scatter(final_df, x="GPA_Numeric", y="Age", color="Cluster",
                      symbol="Gender", title="Clustering Students by GPA and Age")
    st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray;'>"
    "Created with ❤️ by <strong>Ivan Nfinda</strong> | May 2025 | "
    "<a href='https://linkedin.com/in/ivan-nfinda' target='_blank'>LinkedIn</a>"
    "</div>",
    unsafe_allow_html=True
)
