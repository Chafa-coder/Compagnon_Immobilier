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
    layout="wide"
)

# --- BANDEAU VISUEL D'ACCUEIL ---
st.markdown("""
<style>
/* Bandeau principal */
.header-box {
    background-color: #e2e8f0;
    padding: 1rem;
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

</style>

<div class="header-box">
    <div class="header-text">
        <div class="main-title">Compagnon Immobilier</div>
        <div class="subtitle">
        <p>
        Projet DataScientest : octobre - décembre 2025<br>
        </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- CONTENU INTRODUCTIF ---
st.markdown("""
### Objectifs
##### 1. Évaluer le prix d’un bien immobilier
##### 2. Prédire l’évolution du prix au m2 dans le temps selon les territoires.

### Pipeline analytique
1. Exploration et structuration  
2. Nettoyage et feature engineering  
3. Modélisation du prix d’un bien  
4. Prévision temporelle des prix  
5. Synthèse & perspectives

### Données
- Données DVF (Demandes de Valeurs Foncières) 2024-2025 pour l'évaluation du prix de biens (volumétrie ~5M)
- Données DVF 2020-2025 pour l’évolution du prix au m2 dans le temps (Volumétrie ~20M )


_=> Navigation : Utilisez le **menu latéral** pour explorer les différentes étapes du projet._
""")


