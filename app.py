
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="🚀 AI & Statistics Dashboard", layout="wide")

# --- CSS Magic for visual sparkle ---
st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    h1 {
        color: #0a3d62;
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #4fc3f7; }
        to { text-shadow: 0 0 20px #00cec9; }
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Load data ---
df = pd.read_csv("Statistics_Undergraduate_Programs_Ankara.csv")

# --- Filters ---
st.sidebar.header("🎛️ Filters")
universities = st.sidebar.multiselect("University", df["University"].unique(), default=list(df["University"].unique()))
genders = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=list(df["Gender"].unique()))
years = st.sidebar.multiselect("Year of Study", df["Year of Study"].unique(), default=list(df["Year of Study"].unique()))

filtered_df = df.copy()
if universities:
    filtered_df = filtered_df[filtered_df["University"].isin(universities)]
if genders:
    filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]
if years:
    filtered_df = filtered_df[filtered_df["Year of Study"].isin(years)]

# --- Title ---
st.markdown("<h1>📊 Statistics Students & Artificial Intelligence in Ankara</h1>", unsafe_allow_html=True)
st.markdown("### Explore how AI is influencing student perspectives in the field of statistics. Interactive, stylish, and insightful.")

st.markdown(f"**Total Responses Shown:** {len(filtered_df)}")

# --- Tabs for views ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🤖 AI & Careers", "📚 Education", "📋 Data Table"])

# --- Tab 1: Overview ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if not filtered_df.empty:
            fig_gender = px.pie(filtered_df, names="Gender", hole=0.5,
                                title="Gender Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_gender, use_container_width=True)
        else:
            st.warning("No data for gender chart.")

    with col2:
        if not filtered_df.empty:
            uni_counts = filtered_df["University"].value_counts().reset_index()
            uni_counts.columns = ["University", "Count"]
            fig_uni = px.bar(uni_counts, x="University", y="Count", color="Count",
                             title="Students by University", color_continuous_scale="Blues")
            st.plotly_chart(fig_uni, use_container_width=True)
        else:
            st.warning("No data for university chart.")

# --- Tab 2: AI & Careers ---
with tab2:
    if not filtered_df.empty:
        st.subheader("Knowledge Level in AI")
        fig_ai = px.histogram(filtered_df, x="AI and Automation Knowledge Level", color="Gender",
                              barmode="group", title="AI Knowledge by Gender",
                              color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig_ai, use_container_width=True)

        most_knowledge = filtered_df["AI and Automation Knowledge Level"].mode()[0]
        st.info(f"🧠 Most common AI knowledge level: **{most_knowledge}**")

        st.subheader("Perceived Career Impact from AI")
        impact_df = filtered_df["Impact of AI on Career Plans"].value_counts().reset_index()
        impact_df.columns = ["Impact", "Count"]
        fig_impact = px.bar(impact_df, x="Impact", y="Count", color="Impact",
                            title="AI Impact on Career Plans", color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_impact, use_container_width=True)
    else:
        st.warning("No data for this section.")

# --- Tab 3: Education ---
with tab3:
    if not filtered_df.empty:
        st.subheader("Satisfaction with Studying Statistics")
        fig_satis = px.pie(filtered_df, names="Satisfaction with Studying Statistics",
                           title="Satisfaction Levels", hole=0.5,
                           color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_satis, use_container_width=True)

        st.subheader("Does Curriculum Help Adapt to AI?")
        adapt_df = filtered_df["Statistics Curriculum Helps Adapt"].value_counts().reset_index()
        adapt_df.columns = ["Response", "Count"]
        fig_adapt = px.bar(adapt_df, x="Response", y="Count", color="Response",
                           title="Curriculum & AI Adaptability", color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_adapt, use_container_width=True)
    else:
        st.warning("No data for this section.")

# --- Tab 4: Data Table ---
with tab4:
    if not filtered_df.empty:
        st.subheader("📋 Filtered Data Table")
        st.dataframe(filtered_df.style.highlight_max(axis=0), use_container_width=True)
        csv_download = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Data as CSV", data=csv_download, file_name="filtered_data.csv", mime="text/csv")
    else:
        st.warning("No data to display.")

# --- Footer ---
st.markdown("---")
st.markdown("✨ *Crafted with love by **IVAN NFINDA*** using Streamlit & Plotly.")
st.markdown("📬 Let's connect on [LinkedIn](https://www.linkedin.com) and talk data, AI & dashboards!")
st.markdown("✨ *Crafted for data lovers. Share it, remix it, make it yours.*")
st.markdown("📬 Want to connect? Drop a comment on [LinkedIn](https://linkedin.com) 💬")
