
# --- Inject Custom CSS ---
st.markdown("""<style>
/* 🌟 CSS EXTRÊMEMENT SOIGNÉ POUR UN TABLEAU DE BORD ÉLITE */

/* Fond général doux avec dégradé */
body, .main {
    background: linear-gradient(135deg, #f7faff 0%, #eef2f7 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1e293b;
}

/* Animation du titre au survol */
.dashboard-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(255,255,255,0.6);
    transition: all 0.4s ease-in-out;
}

.dashboard-title:hover {
    text-shadow: 0 0 30px rgba(255,255,255,0.9), 0 0 10px #60a5fa;
    transform: scale(1.03);
}

/* Animation de lumière sur titre container */
.title-container {
    background: linear-gradient(120deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.title-container::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.25) 50%, rgba(255,255,255,0) 100%);
    transform: rotate(30deg);
    animation: glowline 6s infinite;
}

@keyframes glowline {
    0% { transform: translateX(-100%) rotate(30deg); }
    50% { transform: translateX(100%) rotate(30deg); }
    100% { transform: translateX(100%) rotate(30deg); }
}

/* Sous-titre raffiné */
.dashboard-subtitle {
    color: #cbd5e1;
    font-size: 1.25rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Cartes KPI avec hover magique */
.info-card {
    background-color: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    transition: all 0.4s ease;
}

.info-card:hover {
    transform: scale(1.03);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* Onglets modernisés */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #e2e8f0;
    border-radius: 10px 10px 0 0;
    padding: 10px 24px;
    font-weight: 600;
    color: #1e3a8a;
    transition: background 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
}

/* Bouton amélioré */
.stDownloadButton button {
    background: linear-gradient(to right, #3b82f6, #2563eb);
    color: white;
    font-weight: 600;
    padding: 0.5rem 1.2rem;
    border-radius: 10px;
    border: none;
    transition: background 0.3s ease;
}

.stDownloadButton button:hover {
    background: linear-gradient(to right, #2563eb, #1d4ed8);
    box-shadow: 0 0 15px rgba(37,99,235,0.3);
}

/* Footer boosté */
footer {
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    padding: 2rem;
    color: white;
    border-radius: 12px;
    text-align: center;
    margin-top: 4rem;
    font-size: 1rem;
}
</style>""", unsafe_allow_html=True)
/mnt/data/streamlit_ai_dashboard_IVAN_CUSTOM.zip


# --- Footer ---
st.markdown("---")
st.markdown("""
<footer>
    <p style='font-size:1.1rem;'>✨ Ce tableau de bord a été conçu avec soin par <strong>IVAN NFINDA</strong></p>
    <p style='font-size:0.95rem;'>🔗 Connectons-nous sur <a href='https://www.linkedin.com' target='_blank' style='color:#93c5fd;'>LinkedIn</a> | 📧 Contact : ivan.nfinda@example.com</p>
</footer>
""", unsafe_allow_html=True)
