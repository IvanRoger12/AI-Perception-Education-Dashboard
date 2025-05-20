import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import base64

st.set_page_config(page_title="🎓 AI Education Dashboard", layout="wide")

# CSS for dark mode toggle (basic)
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f7fa;
    }
    h1 {
        color: #1E3A8A;
    }
    .stat-box {
        background: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 AI & Statistics Student Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")
    gpa_map = {
        "2.00 or below": 1.75,
        "2.01 - 2.50": 2.25,
        "2.51 - 3.00": 2.75,
        "3.01 - 3.50": 3.25,
        "3.51 - 4.00": 3.75
    }
    df["GPA_Numeric"] = df["GPA"].map(gpa_map)
    return df

df = load_data()

st.sidebar.title("🔎 Filters")
selected_uni = st.sidebar.multiselect("University", options=df["University"].unique(), default=df["University"].unique())
selected_gender = st.sidebar.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique())

filtered_df = df[df["University"].isin(selected_uni) & df["Gender"].isin(selected_gender)]

st.subheader("📊 GPA Distribution by University")
fig = px.box(filtered_df, x="University", y="GPA_Numeric", color="University")
st.plotly_chart(fig, use_container_width=True)

# KMeans clustering
st.subheader("🧠 Clustering Students by GPA & Year")
cluster_df = filtered_df.copy()
cluster_df = cluster_df.dropna(subset=["GPA_Numeric", "Year of Study"])
scaler = StandardScaler()
X = scaler.fit_transform(cluster_df[["GPA_Numeric"]])

kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
cluster_df["Cluster"] = kmeans.labels_
fig_cluster = px.scatter(cluster_df, x="GPA_Numeric", y="Age", color="Cluster", title="Clusters")
st.plotly_chart(fig_cluster, use_container_width=True)

# Export options
st.subheader("📄 Export Options")
if st.button("📤 Download Filtered Data (CSV)"):
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)