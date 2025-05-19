

# --- AFFICHAGE MINIMAL POUR TEST --- #
st.markdown("## 🎯 *Aperçu des données filtrées*")

if filtered_df.empty:
    st.warning("⚠️ Aucun résultat avec les filtres actuels.")
else:
    st.dataframe(filtered_df.head())

    st.markdown("### 📊 Répartition par université")
    uni_counts = filtered_df["University"].value_counts().reset_index()
    uni_counts.columns = ["University", "Count"]
    fig_uni = px.bar(uni_counts, x="University", y="Count", title="Nombre d'étudiants par université")
    st.plotly_chart(fig_uni, use_container_width=True)


# --- FOOTER --- #
st.markdown("""
<hr style='margin-top: 50px; margin-bottom:10px;'>

<div style='text-align:center; color:#888; font-size: 0.9rem'>
    Développé avec ❤️ par <strong>IVAN NFINDA</strong><br>
    Retrouvez-moi sur <a href="https://www.linkedin.com/in/ivan-nfinda" target="_blank">LinkedIn</a> · <a href="mailto:ivan@example.com">Contact</a><br>
    <br>
    📅 Dernière mise à jour : Mai 2025
</div>
""", unsafe_allow_html=True)
