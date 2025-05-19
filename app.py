
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="AI & Education Dashboard", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")
    return df

df = load_data()

# Titre
st.title("🎓 AI & Education Dashboard")

# Filtres
st.sidebar.header("Filters")
universities = ["All"] + sorted(df["University"].dropna().unique().tolist())
selected_uni = st.sidebar.selectbox("University", universities)

fields = ["All"] + sorted(df["Field"].dropna().unique().tolist()) if "Field" in df.columns else []
selected_field = st.sidebar.selectbox("Field of Study", fields) if fields else "All"

# Application des filtres
filtered_df = df.copy()
if selected_uni != "All":
    filtered_df = filtered_df[filtered_df["University"] == selected_uni]

if fields and selected_field != "All":
    filtered_df = filtered_df[filtered_df["Field"] == selected_field]

# Affichage
st.markdown("### 🎯 Filtered Dataset")
if filtered_df.empty:
    st.warning("⚠️ No data for the selected filters.")
else:
    st.dataframe(filtered_df)

    if "University" in filtered_df.columns:
        fig1 = px.histogram(filtered_df, x="University", title="Students per University")
        st.plotly_chart(fig1, use_container_width=True)

    if "AI and Automation Knowledge Level" in filtered_df.columns:
        fig2 = px.bar(filtered_df["AI and Automation Knowledge Level"].value_counts().reset_index(),
                      x="index", y="AI and Automation Knowledge Level",
                      labels={"index": "Knowledge Level", "AI and Automation Knowledge Level": "Count"},
                      title="AI Knowledge Levels")
        st.plotly_chart(fig2, use_container_width=True)
