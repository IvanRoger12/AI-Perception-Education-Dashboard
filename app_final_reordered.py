import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import base64
from io import BytesIO
import matplotlib.pyplot as plt

# ----- Setup -----
st.set_page_config(page_title="🎓 Multilingual Education Dashboard", layout="wide")

# ----- Multilingual Support -----
lang = st.sidebar.selectbox("🌐 Language / Langue / Idioma / 语言 / Lingua", ["Français", "English", "Español", "Italiano", "中文"])

translations = {
    "Français": {
        "title": "📊 Analyse complète des étudiants à Ankara",
        "filters": "🎛️ Filtres",
        "students": "👨‍🎓 Total Étudiants",
        "universities": "🏫 Universités",
        "gpa": "🎯 GPA Moyen",
        "ai": "🤖 Connaissance IA",
        "animated": "📽️ Répartition genrée animée par année",
        "bar": "GPA moyen par université et genre",
        "violin": "Distribution GPA par année d'étude",
        "clustering": "🧠 Regroupement des étudiants (GPA & IA)",
        "summary": "📋 Résumé automatique par cluster",
        "export": "📤 Exporter les données",
        "download_csv": "⬇️ Télécharger CSV",
        "download_pdf": "⬇️ Télécharger PDF",
        "raw_data": "🔍 Données brutes",
        "feedback": "📝 Donnez-nous votre avis !"
    },
    "English": {
        "title": "📊 Comprehensive Student Analysis in Ankara",
        "filters": "🎛️ Filters",
        "students": "👨‍🎓 Total Students",
        "universities": "🏫 Universities",
        "gpa": "🎯 Average GPA",
        "ai": "🤖 AI Knowledge",
        "animated": "📽️ Animated Gender Distribution by Year",
        "bar": "Average GPA by University and Gender",
        "violin": "GPA Distribution by Study Year",
        "clustering": "🧠 Student Clustering (GPA & AI)",
        "summary": "📋 Cluster Summary",
        "export": "📤 Export Data",
        "download_csv": "⬇️ Download CSV",
        "download_pdf": "⬇️ Download PDF",
        "raw_data": "🔍 Raw Data",
        "feedback": "📝 Leave your feedback!"
    },
    "Español": {
        "title": "📊 Análisis completo de estudiantes en Ankara",
        "filters": "🎛️ Filtros",
        "students": "👨‍🎓 Total Estudiantes",
        "universities": "🏫 Universidades",
        "gpa": "🎯 Promedio GPA",
        "ai": "🤖 Conocimiento en IA",
        "animated": "📽️ Distribución de género animada por año",
        "bar": "GPA promedio por universidad y género",
        "violin": "Distribución de GPA por año de estudio",
        "clustering": "🧠 Agrupamiento de estudiantes (GPA & IA)",
        "summary": "📋 Resumen por grupo",
        "export": "📤 Exportar datos",
        "download_csv": "⬇️ Descargar CSV",
        "download_pdf": "⬇️ Descargar PDF",
        "raw_data": "🔍 Datos sin procesar",
        "feedback": "📝 ¡Déjanos tu opinión!"
    },
    "Italiano": {
        "title": "📊 Analisi completa degli studenti ad Ankara",
        "filters": "🎛️ Filtri",
        "students": "👨‍🎓 Studenti totali",
        "universities": "🏫 Università",
        "gpa": "🎯 GPA medio",
        "ai": "🤖 Conoscenza IA",
        "animated": "📽️ Distribuzione di genere animata per anno",
        "bar": "GPA medio per università e genere",
        "violin": "Distribuzione GPA per anno di studio",
        "clustering": "🧠 Clustering degli studenti (GPA & IA)",
        "summary": "📋 Riepilogo dei cluster",
        "export": "📤 Esporta dati",
        "download_csv": "⬇️ Scarica CSV",
        "download_pdf": "⬇️ Scarica PDF",
        "raw_data": "🔍 Dati grezzi",
        "feedback": "📝 Lascia il tuo feedback!"
    },
    "中文": {
        "title": "📊 安卡拉学生数据分析仪表盘",
        "filters": "🎛️ 筛选条件",
        "students": "👨‍🎓 学生总数",
        "universities": "🏫 大学数量",
        "gpa": "🎯 平均绩点",
        "ai": "🤖 人工智能知识",
        "animated": "📽️ 按年份划分的性别分布动画",
        "bar": "按大学和性别划分的平均GPA",
        "violin": "按学习年份划分的GPA分布",
        "clustering": "🧠 学生聚类（GPA和AI）",
        "summary": "📋 聚类摘要",
        "export": "📤 导出数据",
        "download_csv": "⬇️ 下载 CSV",
        "download_pdf": "⬇️ 下载 PDF",
        "raw_data": "🔍 原始数据",
        "feedback": "📝 提交反馈意见"
    }
}
t = translations[lang]

# ----- Dark Mode -----
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
st.markdown(f"""
    <style>
        .main, .stApp {{
            background-color: {'#1e1e1e' if dark_mode else '#f9fafb'};
            color: {'white' if dark_mode else 'black'};
        }}
    </style>
""", unsafe_allow_html=True)
template_style = "plotly_dark" if dark_mode else "plotly_white"

# ----- Load Data -----
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

# ----- Filters -----
st.sidebar.header(t["filters"])
univ = st.sidebar.multiselect("University", df["University"].unique(), default=df["University"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
year = st.sidebar.multiselect("Year", df["Year of Study"].unique(), default=df["Year of Study"].unique())

filtered_df = df[
    df["University"].isin(univ) &
    df["Gender"].isin(gender) &
    df["Year of Study"].isin(year)
]

# ----- Header -----
st.title(t["title"])

# ----- KPIs -----
col1, col2, col3, col4 = st.columns(4)
col1.metric(t["students"], len(filtered_df))
col2.metric(t["universities"], filtered_df["University"].nunique())
col3.metric(t["gpa"], round(filtered_df["GPA_Numeric"].mean(), 2) if not filtered_df.empty else 0)
col4.metric(t["ai"], filtered_df["AI and Automation Knowledge Level"].mode()[0] if not filtered_df.empty else "N/A")

# ----- Graphs -----
st.subheader(t["animated"])
fig1 = px.histogram(filtered_df, x="Gender", animation_frame="Year of Study", color="Gender", barmode="group", template=template_style)
st.plotly_chart(fig1, use_container_width=True)

st.subheader(t["bar"])
fig2 = px.bar(filtered_df, x="University", y="GPA_Numeric", color="Gender", template=template_style)
st.plotly_chart(fig2, use_container_width=True)

st.subheader(t["violin"])
fig3 = px.violin(filtered_df, y="GPA_Numeric", x="Year of Study", color="Gender", box=True, template=template_style)
st.plotly_chart(fig3, use_container_width=True)

# ----- Clustering -----
st.subheader(t["clustering"])
if not filtered_df.empty:
    data = filtered_df[["GPA_Numeric"]].copy()
    data["AI_Knowledge"] = filtered_df["AI and Automation Knowledge Level"].astype("category").cat.codes
    X_scaled = StandardScaler().fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    data["Cluster"] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    data[["PC1", "PC2"]] = pca.fit_transform(X_scaled)

    fig4 = px.scatter(data, x="PC1", y="PC2", color=data["Cluster"].astype(str), template=template_style)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(t["summary"])
    for cluster in sorted(data["Cluster"].unique()):
        c = data[data["Cluster"] == cluster]
        st.write(f"🔹 Cluster {cluster}: {len(c)} students | Avg GPA: {c['GPA_Numeric'].mean():.2f} | Avg AI: {c['AI_Knowledge'].mean():.2f}")

# ----- Export -----
st.subheader(t["export"])
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(t["download_csv"], csv, "filtered_data.csv", "text/csv")

def create_pdf(df):
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(8, len(df)/3))
    ax.axis("off")
    ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')
    plt.tight_layout()
    plt.savefig(buf, format="pdf")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

pdf_link = create_pdf(filtered_df)
st.markdown(f'<a href="data:application/pdf;base64,{pdf_link}" download="filtered_data.pdf">{t["download_pdf"]}</a>', unsafe_allow_html=True)


# ----- More Interactive and Relevant Visuals -----
st.subheader("📊 Additional Insights")

col1, col2 = st.columns(2)
with col1:
    fig5 = px.sunburst(filtered_df, path=["University", "Year of Study", "Gender"], values="GPA_Numeric",
                       title="Sunburst: GPA by University, Year, and Gender", template=template_style)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    fig6 = px.treemap(filtered_df, path=["Gender", "University"], values="GPA_Numeric",
                      title="Treemap: GPA Contribution by Gender and University", template=template_style)
    st.plotly_chart(fig6, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig7 = px.scatter(filtered_df, x="GPA_Numeric", y="Year of Study", color="Gender",
                      title="Scatter: GPA vs Year of Study by Gender", template=template_style)
    st.plotly_chart(fig7, use_container_width=True)

with col4:
    if "AI and Automation Knowledge Level" in filtered_df.columns:
        ai_order = filtered_df["AI and Automation Knowledge Level"].value_counts().index.tolist()
        fig8 = px.bar(filtered_df, x="AI and Automation Knowledge Level", color="Gender",
                      title="Bar Chart: AI Knowledge by Gender", template=template_style, category_orders={"AI and Automation Knowledge Level": ai_order})
        st.plotly_chart(fig8, use_container_width=True)



# ----- Export -----
st.subheader(t["export"])
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(t["download_csv"], csv, "filtered_data.csv", "text/csv")

def create_pdf(df):
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(8, len(df)/3))
    ax.axis("off")
    ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')
    plt.tight_layout()
    plt.savefig(buf, format="pdf")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

pdf_link = create_pdf(filtered_df)
st.markdown(f'<a href="data:application/pdf;base64,{pdf_link}" download="filtered_data.pdf">{t["download_pdf"]}</a>', unsafe_allow_html=True)


# ----- More Interactive and Relevant Visuals -----
st.subheader("📊 Additional Insights")

col1, col2 = st.columns(2)
with col1:
    fig5 = px.sunburst(filtered_df, path=["University", "Year of Study", "Gender"], values="GPA_Numeric",
                       title="Sunburst: GPA by University, Year, and Gender", template=template_style)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    fig6 = px.treemap(filtered_df, path=["Gender", "University"], values="GPA_Numeric",
                      title="Treemap: GPA Contribution by Gender and University", template=template_style)
    st.plotly_chart(fig6, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig7 = px.scatter(filtered_df, x="GPA_Numeric", y="Year of Study", color="Gender",
                      title="Scatter: GPA vs Year of Study by Gender", template=template_style)
    st.plotly_chart(fig7, use_container_width=True)

with col4:
    if "AI and Automation Knowledge Level" in filtered_df.columns:
        ai_order = filtered_df["AI and Automation Knowledge Level"].value_counts().index.tolist()
        fig8 = px.bar(filtered_df, x="AI and Automation Knowledge Level", color="Gender",
                      title="Bar Chart: AI Knowledge by Gender", template=template_style, category_orders={"AI and Automation Knowledge Level": ai_order})
        st.plotly_chart(fig8, use_container_width=True)


# ----- Raw Data -----

# ----- Final Analysis Summary -----
st.subheader("🧾 Final Summary")
st.markdown("""
Voici une synthèse finale de l'analyse des étudiants :

- Le GPA moyen est **{:.2f}** pour un total de **{}** étudiants.
- Le niveau de connaissance en IA le plus fréquent est **{}**.
- Les clusters identifiés révèlent des groupes distincts selon le GPA et la connaissance en IA.

🔍 Utilisez les filtres pour explorer d'autres patterns dans les données.
""".format(
    round(filtered_df["GPA_Numeric"].mean(), 2) if not filtered_df.empty else 0,
    len(filtered_df),
    filtered_df["AI and Automation Knowledge Level"].mode()[0] if not filtered_df.empty else "N/A"
))

# ----- User Feedback Form -----
st.subheader("💬 Feedback & Suggestions")
with st.form("feedback_form"):
    name = st.text_input("Votre nom / Your name")
    comment = st.text_area("Laissez un commentaire ou une suggestion / Leave a comment or suggestion")
    submitted = st.form_submit_button("Envoyer / Submit")
    if submitted:
        st.success("Merci pour votre retour ! / Thank you for your feedback!")

# ----- LinkedIn Share -----
st.markdown("---")
st.markdown("🔗 **Partagez ce tableau de bord sur LinkedIn !**")
linkedin_text = (
    "Découvrez ce tableau de bord interactif sur la perception de l'IA en éducation, "
    "avec analyse des étudiants à Ankara, clustering, visualisations dynamiques et plus encore ! "
    "#DataScience #Streamlit #Éducation #IA"
)
share_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://ai-perception-education-dashboard-mmebrs32g7nhabggb9znsp.streamlit.app"
st.markdown(f"[Partager sur LinkedIn]({share_url})", unsafe_allow_html=True)

st.subheader(t["raw_data"])
st.dataframe(filtered_df)

# ----- Feedback -----
st.sidebar.markdown("---")
st.sidebar.text_area(t["feedback"])