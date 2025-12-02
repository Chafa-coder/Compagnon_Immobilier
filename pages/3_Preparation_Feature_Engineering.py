

import streamlit as st
import pandas as pd
import os
import glob
import plotly.graph_objects as go
from pathlib import Path

# ======================================
# PAGE : 3_Preparation_Feature_Engineering
# ======================================
st.set_page_config(page_title="Préparation & Feature Engineering", layout="wide")

st.title("🧩 Préparation & Feature Engineering")
st.markdown("""
Cette page présente la **volumétrie** du dataset DVF, la **réduction progressive** au fil des filtres, 
et l'analyse des **outliers sur la valeur foncière et les surfaces**.
""")

# ============================
# 🔹 Chargement des outputs
# ============================
# output_dir = r"C:\Users\cbent\Projets\data\outputs_prepa"

output_dir = Path("data") / "outputs_prepa"

# Vérification de la présence minimale
required_files = ["stats_volumes.csv", "boxplot_valeur_fonciere_avant.png"]
missing_files = [f for f in required_files if not os.path.exists(os.path.join(output_dir, f))]

if missing_files:
    st.error(f"❌ Fichiers manquants : {', '.join(missing_files)}\n\nExécute le notebook de préparation avant de continuer.")
    st.stop()

# --- Chargement des stats volumétrie ---
stats_volumes = pd.read_csv(os.path.join(output_dir, "stats_volumes.csv")).iloc[0]


# ============================
# 🔹 Tabs : Valeur foncière / Surface utilisée
# ============================
tab1, tab2 = st.tabs(["💶 Valeur foncière", "🏠 Surface utilisée"])

# --------------------------------------------------------------------
# 1️⃣ Valeur foncière
# --------------------------------------------------------------------
with tab1:
    st.subheader("Gestion des valeurs extrêmes")

    # Afficher "avant" puis "après" dans le bon ordre
    img_avant = os.path.join(output_dir, "boxplot_valeur_fonciere_avant.png")
    img_apres = os.path.join(output_dir, "boxplot_valeur_fonciere_apres.png")

    col1, col2 = st.columns(2)
    if os.path.exists(img_avant):
        col1.markdown("**Avant suppression des outliers**")
        col1.image(img_avant, use_container_width=True)
    if os.path.exists(img_apres):
        col2.markdown("**Après suppression des outliers**")
        col2.image(img_apres, use_container_width=True)

# --------------------------------------------------------------------
# 2️⃣ Surface utilisée
# --------------------------------------------------------------------
with tab2:
    st.subheader("Distribution des surfaces utilisées")

    

    # Recherche des images surface
    avant_img = os.path.join(output_dir, "boxplot_surface_avant.png")
    apres_img = os.path.join(output_dir, "boxplot_surface_apres.png")

    col1, col2 = st.columns(2)
    if os.path.exists(avant_img):
        col1.markdown("**Avant suppression des outliers**")
        col1.image(avant_img, use_container_width=True)
    if os.path.exists(apres_img):
        col2.markdown("**Après suppression des outliers**")
        col2.image(apres_img, use_container_width=True)
        
        
        
# ============================
# 🔹 Tabs : Valeur foncière / Surface utilisée
# ============================
tab1, tab2 = st.tabs(["💶 Réduction volumétrie", "🏠 Réduction colonnes"])

# --------------------------------------------------------------------
# 1️⃣ Antonoire lignes
# --------------------------------------------------------------------
with tab1:

    st.subheader("🧮 Réduction progressive du dataset DVF")
    funnel_html_path = os.path.join(output_dir, "fig.html")

    if os.path.exists(funnel_html_path):
        with open(funnel_html_path, "r", encoding="utf-8") as f:
            html = f.read()
        st.components.v1.html(html, height=500)
    else:
        st.warning("Fichier funnel HTML non trouvé.")

    st.markdown("---")
    
    
# --------------------------------------------------------------------
# 2️⃣ ntonoire colonnes
# --------------------------------------------------------------------

with tab2:
    st.subheader("Réduction progressive du nombre de colonnes")

    # -------------------------
    # Étapes de transformation du dataset
    etapes = [
        "Fichier brut",
        "quasi vides et non exploitable",
        "Redondantes ou non pertinentes pour modélisation ",
        "Retenues pour modélisation"
    ]
    # Nombre de lignes après chaque étape
    lignes = [
        40,
        28,
        15,
        10
    ]
    # Palette dégradée de bleus (foncé → clair)
    colors = [
        "#0B3D91",
        "#1556B0",
        "#1E6FCC",
        "#2B84E0"
    ]

    # Création du funnel avec Plotly
    fig = go.Figure(go.Funnel(
        y = etapes,
        x = lignes,
        textinfo = "value",
        textposition = "inside",
        texttemplate = "%{value}",  # valeurs toujours affichées
        opacity = 0.9,
        marker = {
            "color": colors,
            "line": {"color": "white", "width": 1}
        }
    ))

    fig.update_layout(
        title="Réduction progressive du nombre de colonnes",
        xaxis_title="Nombre de lignes restantes",
        height=500,
        width=500,  # largeur fixe
        font=dict(size=12),
        plot_bgcolor="white",
    )

    # Utilisation des colonnes pour contrôler la largeur
    col1, col2 = st.columns([1, 1])  # ajuster ratio pour élargir ou réduire
    with col1:
        st.plotly_chart(fig)  # width défini dans layout, pas use_container_width

    st.markdown("---")

