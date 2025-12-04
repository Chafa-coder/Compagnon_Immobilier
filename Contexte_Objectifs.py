# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 08:45:38 2025

@author: cbent
"""

import streamlit as st

# -----------
# import os
# import sys

# st.write("Python executable:", sys.executable)
# st.write("Environment PATH:", os.environ.get("PATH"))
# ---------------------

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Overview du projet",
    # page_icon="🏠",
    layout="wide"
)

# --- BANDEAU VISUEL D'ACCUEIL ---
st.markdown("""
<style>
/* Bandeau principal */
.header-box {
    background-color: #e2e8f0;
    padding: 2rem;
    border-radius: 1rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 2rem;
}

/* Texte du bandeau */
.header-text {
    flex: 1;
}

.header-text .main-title {
    font-size: 2rem;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 0.3rem;
}

.header-text .subtitle {
    font-size: 1.1rem;
    color: #475569;
    margin-top: -0.3rem;
}

/* Image/logo du bandeau */
.header-img {
    width: 220px;
    border-radius: 1rem;
    opacity: 0.95;
}
</style>

<div class="header-box">
    <div class="header-text">
        <div class="main-title">Compagnon Immobilier</div>
        <div class="subtitle">Estimation & prévision du marché immobilier français</div>
        <p>
        Utilisation des données ouvertes 
        <b>Demandes de Valeurs Foncières (DVF)</b>.<br>
        Découvrez comment la donnée permet d’évaluer les biens et d’anticiper les tendances du marché.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
#      <img class="header-img" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Real_estate_icon.svg/512px-Real_estate_icon.svg.png" />
# </div>
# """, unsafe_allow_html=True)

# --- CONTENU INTRODUCTIF ---
st.markdown("""
### Objectifs
**1. Évaluer le prix d’un bien immobilier**.  
**2.	Prédire l’évolution du prix au m2 dans le temps** selon les territoires.

### Pipeline analytique
1. Exploration & traitements de 1er niveau du fichier DVF  
2. Préparation avancée & Feature Engineering  
3. Modélisation du prix d’un bien  
4. Prévision temporelle des prix  
5. Synthèse & perspectives

### Navigation
➡️ Utilisez le **menu latéral** pour explorer les différentes étapes du projet.
""")

# st.info("💡 Tout calcul lourd (nettoyage, entraînement de modèles, projections) est réalisé en amont. L’application se concentre sur l’exploration, la visualisation et l’interprétation.")
