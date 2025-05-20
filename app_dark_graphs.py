
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import base64
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="🎓 Education Dashboard - Ivan Nfinda", layout="wide")

# Dark mode toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

def add_custom_css(dark):
    if dark:
        st.markdown("""
        <style>
            .main, .stApp {
                background-color: #1e1e1e;
                color: white;
            }
            .css-1v3fvcr {
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .main, .stApp {
                background-color: #f9fafb;
                color: black;
            }
            .css-1v3fvcr {
                color: black;
            }
        </style>
        """, unsafe_allow_html=True)

add_custom_css(dark_mode)
template_style = "plotly_dark" if dark_mode else "plotly_white"

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

# Animated Chart
st.subheader("📽️ Animated Gender Distribution by Year")
animated_fig = px.histogram(filtered_df, x="Gender", animation_frame="Year of Study", color="Gender", barmode="group", template=template_style)
st.plotly_chart(animated_fig, use_container_width=True)

# Additional Charts
st.subheader("📈 Additional Visualizations")
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(filtered_df, x="University", y="GPA_Numeric", color="Gender", title="Average GPA by University and Gender", template=template_style)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.violin(filtered_df, y="GPA_Numeric", x="Year of Study", color="Gender", box=True, title="GPA Distribution by Study Year", template=template_style)
    st.plotly_chart(fig, use_container_width=True)

# Clustering Section
st.subheader("🧠 Student Clustering (GPA & AI Knowledge)")
if not filtered_df.empty:
    clustering_df = filtered_df[["GPA_Numeric"]].copy()
    clustering_df["AI_Knowledge"] = filtered_df["AI and Automation Knowledge Level"].astype("category").cat.codes

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(clustering_df)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clustering_df["Cluster"] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    clustering_df["PC1"], clustering_df["PC2"] = components[:,0], components[:,1]

    cluster_fig = px.scatter(clustering_df, x="PC1", y="PC2", color=clustering_df["Cluster"].astype(str), title="Cluster Visualization", template=template_style)
    st.plotly_chart(cluster_fig, use_container_width=True)

    # Résumé automatique
    st.markdown("📋 **Cluster Summary**")
    for cluster in sorted(clustering_df["Cluster"].unique()):
        count = (clustering_df["Cluster"] == cluster).sum()
        avg_gpa = clustering_df[clustering_df["Cluster"] == cluster]["GPA_Numeric"].mean()
        avg_ai = clustering_df[clustering_df["Cluster"] == cluster]["AI_Knowledge"].mean()
        st.write(f"🔹 Cluster {cluster}: {count} students | Avg GPA: {round(avg_gpa,2)} | Avg AI Knowledge (encoded): {round(avg_ai,2)}")

# Export options
st.subheader("📤 Export Data")
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

csv = convert_df(filtered_df)
st.download_button("⬇️ Download CSV", csv, "filtered_data.csv", "text/csv")

# Export as PDF (basic with table only)
def create_pdf_download_link(df):
    buffer = BytesIO()
    fig, ax = plt.subplots(figsize=(8, len(df)/3))
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')
    plt.tight_layout()
    plt.savefig(buffer, format="pdf")
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="filtered_data.pdf">⬇️ Download PDF</a>'

st.markdown(create_pdf_download_link(filtered_df), unsafe_allow_html=True)

# Raw Data Table
st.subheader("🔍 Raw Data")
st.dataframe(filtered_df)

st.markdown("---")
st.markdown("💡 **Built with love by Ivan Nfinda | Last updated: May 2025**", unsafe_allow_html=True)
