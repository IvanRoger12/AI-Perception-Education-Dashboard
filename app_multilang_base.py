
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="🌍 Multilingual Dashboard", layout="wide")

# Langue sélectionnée
lang = st.sidebar.selectbox("🌐 Language / Langue", ["English", "Français", "Español", "Italiano", "中文"])

# Traductions
translations = {
    "English": {
        "title": "📊 Comprehensive Student Analysis in Ankara",
        "filters": "🎛️ Filters",
        "students": "👨‍🎓 Total Students",
        "universities": "🏫 Universities",
        "avg_gpa": "🎯 Average GPA",
        "ai_knowledge": "🤖 AI Knowledge",
        "animated_chart": "📽️ Animated Gender Distribution by Year",
        "raw_data": "🔍 Raw Data",
        "export_csv": "⬇️ Download CSV",
        "feedback": "📝 Share your feedback",
    },
    "Français": {
        "title": "📊 Analyse complète des étudiants à Ankara",
        "filters": "🎛️ Filtres",
        "students": "👨‍🎓 Total Étudiants",
        "universities": "🏫 Universités",
        "avg_gpa": "🎯 GPA Moyen",
        "ai_knowledge": "🤖 Connaissance IA",
        "animated_chart": "📽️ Répartition animée par genre et année",
        "raw_data": "🔍 Données Brutes",
        "export_csv": "⬇️ Télécharger CSV",
        "feedback": "📝 Donnez votre avis",
    },
    "Español": {
        "title": "📊 Análisis de estudiantes en Ankara",
        "filters": "🎛️ Filtros",
        "students": "👨‍🎓 Total Estudiantes",
        "universities": "🏫 Universidades",
        "avg_gpa": "🎯 Promedio GPA",
        "ai_knowledge": "🤖 Conocimiento de IA",
        "animated_chart": "📽️ Distribución de género animada por año",
        "raw_data": "🔍 Datos brutos",
        "export_csv": "⬇️ Descargar CSV",
        "feedback": "📝 Comparte tu opinión",
    },
    "Italiano": {
        "title": "📊 Analisi completa degli studenti ad Ankara",
        "filters": "🎛️ Filtri",
        "students": "👨‍🎓 Studenti Totali",
        "universities": "🏫 Università",
        "avg_gpa": "🎯 GPA Medio",
        "ai_knowledge": "🤖 Conoscenza dell'IA",
        "animated_chart": "📽️ Distribuzione di genere animata per anno",
        "raw_data": "🔍 Dati grezzi",
        "export_csv": "⬇️ Scarica CSV",
        "feedback": "📝 Lascia un feedback",
    },
    "中文": {
        "title": "📊 安卡拉学生综合分析",
        "filters": "🎛️ 筛选条件",
        "students": "👨‍🎓 学生总数",
        "universities": "🏫 大学数量",
        "avg_gpa": "🎯 平均 GPA",
        "ai_knowledge": "🤖 人工智能知识",
        "animated_chart": "📽️ 按年划分的性别分布动画图",
        "raw_data": "🔍 原始数据",
        "export_csv": "⬇️ 下载 CSV",
        "feedback": "📝 提供您的反馈",
    },
}

t = translations[lang]

# Mode sombre
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
template_style = "plotly_dark" if dark_mode else "plotly_white"

# Chargement des données
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

# Filtres
st.sidebar.header(t["filters"])
univ = st.sidebar.multiselect("University", df["University"].unique(), default=df["University"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
year = st.sidebar.multiselect("Year of Study", df["Year of Study"].unique(), default=df["Year of Study"].unique())

filtered_df = df[
    df["University"].isin(univ) &
    df["Gender"].isin(gender) &
    df["Year of Study"].isin(year)
]

# Titre
st.title(t["title"])

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric(t["students"], len(filtered_df))
col2.metric(t["universities"], filtered_df["University"].nunique())
col3.metric(t["avg_gpa"], round(filtered_df["GPA_Numeric"].mean(), 2) if not filtered_df.empty else 0)
col4.metric(t["ai_knowledge"], filtered_df["AI and Automation Knowledge Level"].mode()[0] if not filtered_df.empty else "N/A")

# Graphique animé
st.subheader(t["animated_chart"])
animated_fig = px.histogram(filtered_df, x="Gender", animation_frame="Year of Study", color="Gender", barmode="group", template=template_style)
st.plotly_chart(animated_fig, use_container_width=True)

# Export
st.subheader("📤 Export")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(t["export_csv"], csv, "filtered_data.csv", "text/csv")

# Feedback
st.subheader(t["feedback"])
st.text_area("✉️", placeholder="Your thoughts here...")

# Données
st.subheader(t["raw_data"])
st.dataframe(filtered_df)
