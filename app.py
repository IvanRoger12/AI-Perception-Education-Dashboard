import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Éducation - Ivan Nfinda",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
def add_custom_css():
    css = """
    <style>
    body { font-family: 'Poppins', sans-serif; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

add_custom_css()

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")

df = load_data()

st.title("📚 Dashboard Éducation")
st.markdown("### Analyse des performances et statistiques étudiantes")

# Exemple de graphique
st.markdown("## Répartition par université")
uni_counts = df["University"].value_counts().reset_index()
uni_counts.columns = ["University", "Count"]
fig = px.bar(uni_counts, x="University", y="Count", title="Étudiants par université")
st.plotly_chart(fig)