/mnt/data/streamlit_ai_dashboard_IVAN_CUSTOM.zip


# --- Footer ---
st.markdown("---")
st.markdown("""
<footer>
    <p style='font-size:1.1rem;'>✨ Ce tableau de bord a été conçu avec soin par <strong>IVAN NFINDA</strong></p>
    <p style='font-size:0.95rem;'>🔗 Connectons-nous sur <a href='https://www.linkedin.com' target='_blank' style='color:#93c5fd;'>LinkedIn</a> | 📧 Contact : ivan.nfinda@example.com</p>
</footer>
""", unsafe_allow_html=True)


# --- Clustering KMeans (bonus avancé) ---
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

st.markdown("## 🧬 Student Clustering (K-Means)")
features = ['Age', 'GPA']

if len(filtered_df) >= 3:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(filtered_df[features])
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X_scaled)
    filtered_df['Cluster'] = kmeans.labels_

    fig_cluster = px.scatter(
        filtered_df,
        x="Age",
        y="GPA",
        color="Cluster",
        hover_data=["University", "Field"],
        title="Clustering des étudiants (basé sur Age et GPA)",
        color_continuous_scale=px.colors.diverging.Tealrose
    )
    st.plotly_chart(fig_cluster, use_container_width=True)
else:
    st.info("Pas assez de données pour appliquer le clustering.")

# --- Exportation PDF (fonctionnalité simple simulée) ---
import io

st.markdown("### 🧾 Export Data")
buffer = io.StringIO()
filtered_df.to_csv(buffer, index=False)
buffer.seek(0)
st.download_button(
    label="📄 Télécharger les données filtrées en CSV",
    data=buffer,
    file_name="filtered_students.csv",
    mime="text/csv"
)
