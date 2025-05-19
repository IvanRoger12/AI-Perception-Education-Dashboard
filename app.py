
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import io
from fpdf import FPDF

st.set_page_config(page_title="🎓 Education Dashboard - Ivan Nfinda", layout="wide")

def add_custom_css():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
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
st.sidebar.header("🔍 Filters")
univ = st.sidebar.multiselect("University", df["University"].unique(), default=df["University"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
year = st.sidebar.multiselect("Year of Study", df["Year of Study"].unique(), default=df["Year of Study"].unique())

filtered_df = df[
    df["University"].isin(univ) &
    df["Gender"].isin(gender) &
    df["Year of Study"].isin(year)
]

# Header
st.title("📊 Comprehensive Student Dashboard in Ankara")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍🎓 Total Students", len(filtered_df))
col2.metric("🏫 Universities", filtered_df["University"].nunique())
col3.metric("📈 Average GPA", round(filtered_df["GPA_Numeric"].mean(), 2) if not filtered_df.empty else 0)
col4.metric("🤖 Top AI Knowledge Level", filtered_df["AI and Automation Knowledge Level"].mode()[0] if not filtered_df.empty else "N/A")

# Visuals
st.subheader("📌 Demographic Distribution")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(filtered_df, names="Gender", title="Gender Distribution", hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(filtered_df, x="Year of Study", color="University", title="Year of Study by University", animation_frame="Gender")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📚 GPA and AI Knowledge")
col1, col2 = st.columns(2)

with col1:
    fig3 = px.box(filtered_df, x="University", y="GPA_Numeric", title="GPA Distribution per University")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.histogram(filtered_df, x="AI and Automation Knowledge Level", color="Gender", title="AI Knowledge by Gender")
    st.plotly_chart(fig4, use_container_width=True)

# Clustering
st.subheader("🧠 Student Segmentation (Clustering)")
if len(filtered_df) >= 3:
    features = filtered_df[["GPA_Numeric"]].fillna(0)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=3, n_init='auto')
    filtered_df["Cluster"] = kmeans.fit_predict(scaled)

    fig5 = px.scatter(filtered_df, x="GPA_Numeric", y="Age", color="Cluster", symbol="Gender", title="Clustering Students by GPA and Age")
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Not enough data for clustering (need at least 3 students).")

# Export PDF
st.subheader("📤 Export")
if st.button("Export summary to PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Student Data Summary", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    for u in univ:
        pdf.cell(200, 8, f"University: {u}", ln=True)
    pdf.ln(4)
    pdf.cell(200, 8, f"Total Students: {len(filtered_df)}", ln=True)
    pdf.cell(200, 8, f"Average GPA: {round(filtered_df['GPA_Numeric'].mean(), 2) if not filtered_df.empty else 'N/A'}", ln=True)
    pdf.cell(200, 8, f"Top AI Knowledge: {filtered_df['AI and Automation Knowledge Level'].mode()[0] if not filtered_df.empty else 'N/A'}", ln=True)

    pdf_output = "/mnt/data/student_summary.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as f:
        st.download_button("📄 Download PDF", f, file_name="summary.pdf")

# Raw data
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)
