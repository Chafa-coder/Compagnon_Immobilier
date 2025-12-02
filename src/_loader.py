# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 18:33:48 2025

@author: cbent
"""

# src/_loader.py
import streamlit as st
import time

# --- CONFIG GLOBALE ---
st.set_page_config(
    page_title="DVF Insights",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PAGE D’ACCUEIL LÉGÈRE ---
st.markdown("""
<h2 style='text-align:center; color:#1e3a8a;'>🏠 DVF Insights – Analyse et Prévision Immobilière</h2>
<p style='text-align:center; color:gray;'>Chargement de l'application...</p>
""", unsafe_allow_html=True)

progress = st.progress(0)
for i in range(1, 101, 10):
    time.sleep(0.03)
    progress.progress(i)

# --- REDIRECTION AUTOMATIQUE ---
# La page cible doit être le nom du fichier dans pages/ sans le .py
st.switch_page("1_Overview_projet")
