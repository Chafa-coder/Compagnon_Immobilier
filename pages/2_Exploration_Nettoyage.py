import streamlit as st
import pandas as pd
import os
from pathlib import Path

# -----------------------------
# Répertoire des fichiers générés
# -----------------------------
# data_dir = r"C:\Users\cbent\Projets\data"
# data_dir = "data"
data_dir = Path("data") / "Exploration"

st.title("Exploration et nettoyage du dataset DVF")

# -----------------------------
# 1️⃣ Illustration de la structure DVF brute et agrégée
# -----------------------------
st.subheader("Illustration de la structure DVF brute et agrégée")

avant_path = os.path.join(data_dir, "exemple_avant_agreg_appart.csv")
apres_path = os.path.join(data_dir, "exemple_apres_agreg_appart.csv")

if os.path.exists(avant_path) and os.path.exists(apres_path):
    df_avant = pd.read_csv(avant_path)
    df_apres = pd.read_csv(apres_path)
    st.markdown("**Exemple avant agrégation (brut DVF)**")
    st.dataframe(df_avant)
    st.markdown("**Exemple après agrégation par mutation**")
    st.dataframe(df_apres)
else:
    st.warning("Les fichiers d'exemple avant/après agrégation sont introuvables.")

# -----------------------------
# 2️⃣ Top 20 colonnes avec le plus de NaN
# -----------------------------
st.subheader("Top 20 colonnes avec le plus de valeurs manquantes")
nan_img_path = os.path.join(data_dir, "fig_nan_top20.png")
nan_csv_path = os.path.join(data_dir, "nan_top20.csv")

if os.path.exists(nan_img_path):
    st.image(nan_img_path, caption="Top 20 colonnes avec le plus de NaN")
# if os.path.exists(nan_csv_path):
#     df_nan = pd.read_csv(nan_csv_path)
#     st.dataframe(df_nan)
else:
    st.warning("Données NaN non trouvées.")

# -----------------------------
# 3️⃣ Graphique type_local avant / après agrégation
# -----------------------------
st.subheader("Simplification de la variable type_local")

type_img_path = os.path.join(data_dir, "type_local_simplification.png")
if os.path.exists(type_img_path):
    st.image(type_img_path, caption="Comparaison des types de biens avant/après simplification")
else:
    st.warning("Graphique de comparaison non trouvé.")
    
# -----------------------------
# 4️⃣ Nouvelles colonnes créées
# -----------------------------
st.subheader("Nouvelles colonnes créées")
new_cols_csv = os.path.join(data_dir, "nouvelles_colonnes.csv")
if os.path.exists(new_cols_csv):
    df_new_cols = pd.read_csv(new_cols_csv)
    st.write("Les transformations appliquées ont introduit plusieurs variables dérivées utiles pour la suite :")
    st.table(df_new_cols)
else:
    st.warning("Fichier nouvelles_colonnes.csv non trouvé.")

# -----------------------------
# 4️⃣ Remarques / synthèse
# -----------------------------
# st.markdown("""
# ### 🧭 Interprétation :
# - L’agrégation permet de regrouper les biens liés à une même mutation (ex : maison + dépendance).
# - Le nombre total de lignes diminue, mais la cohérence par mutation augmente.
# - Les types locaux sont simplifiés pour les analyses (Maison / Appartement / Dépendance / Mixte).
# """)
