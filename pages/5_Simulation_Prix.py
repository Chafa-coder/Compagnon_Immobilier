# 5_Simulation_Prix.py
import streamlit as st
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
# import time
# import os

st.set_page_config(page_title="5_Simulation_Prix — Estimation Immobilière", layout="wide")
st.title("Estimation immobilière")

# -----------------------
# Paths modèles
# -----------------------
# MODEL_DIR = Path(r"C:\Users\cbent\Projets\data\outputs_modelisation")
MODEL_DIR = Path("data") / "outputs_modelisation"

MODEL_MAISON = MODEL_DIR / "xgb_maison_optim.pkl"
MODEL_APPART = MODEL_DIR / "xgb_appartement_optim.pkl"

# -----------------------
# Chargement modèles (once)
# -----------------------
@st.cache_resource
def load_models():
    models = {}
    errors = {}
    for k, p in [("maison", MODEL_MAISON), ("appart", MODEL_APPART)]:
        if p.exists():
            try:
                models[k] = joblib.load(p)
            except Exception as e:
                models[k] = None
                errors[k] = str(e)
        else:
            models[k] = None
            errors[k] = f"Fichier introuvable: {p}"
    return models, errors

models, model_errors = load_models()

if any(models.values()):
    st.success("Modèle chargé.")
else:
    st.error("Aucun modèle chargé. Vérifiez les fichiers dans outputs_modelisation.")
    for k, e in model_errors.items():
        st.write(f"{k}: {e}")
    st.stop()

# -----------------------
# Helpers: API Gouv pour commune
# -----------------------
def get_commune_from_cp(code_postal: str):
    try:
        url = f"https://geo.api.gouv.fr/communes?codePostal={code_postal}&fields=nom,code,codeDepartement&format=json"
        r = requests.get(url, timeout=4)
        data = r.json()
        if not data:
            return None, None, None
        # prefer exact match if multiple
        commune = data[0]["nom"]
        code_commune = data[0]["code"]
        code_departement = data[0]["codeDepartement"]
        return commune, code_commune, code_departement
    except Exception:
        return None, None, None

def geocode_address(numero, rue, code_postal, commune):
    try:
        geolocator = Nominatim(user_agent="estimation_app")
        address = f"{numero} {rue}, {code_postal} {commune}, France"
        location = geolocator.geocode(address, timeout=10)
        if location:
            return float(location.latitude), float(location.longitude)
        return None, None
    except Exception:
        return None, None

# -----------------------
# UI : Inputs (adresse en plusieurs champs)
# -----------------------
col_addr1, col_addr2 = st.columns([2, 1])

with col_addr1:
    numero = st.text_input("Numéro", value="")
    rue = st.text_input("Nom de la rue", value="")
with col_addr2:
    code_postal = st.text_input("Code postal", value="")
    commune_manual = st.text_input("Commune (optionnel)", value="")

        
col_left, col_right = st.columns([2,1])

with col_left:
    # st.subheader("Caractéristiques du bien")
    type_bien = st.selectbox("Type de bien", ["Maison", "Appartement"])
    surface_habitable = st.number_input("Surface habitable (m²)", min_value=1.0, value=50.0, step=1.0)
    
with col_right:
    nombre_pieces = st.number_input("Nombre de pièces", min_value=1, value=3, step=1)
    surface_terrain = 0.0
    if type_bien == "Maison":
        surface_terrain = st.number_input("Surface terrain (m²)", min_value=0.0, value=0.0, step=1.0)


# -----------------------
# Pré-remplir commune via API si absent
# -----------------------
commune = None
code_commune = None
code_departement = None
if code_postal and len(code_postal) == 5 and code_postal.isdigit():
    c, cc, cd = get_commune_from_cp(code_postal)
    if c:
        commune = c
        code_commune = cc
        code_departement = cd
    else:
        commune = commune_manual if commune_manual else None
else:
    commune = commune_manual if commune_manual else None

# -----------------------
# Bouton prédiction
# -----------------------
if st.button("Estimer le prix"):

    # validations explicites
    errors = []
    if surface_habitable is None or surface_habitable <= 0:
        errors.append("Surface habitable doit être > 0.")
    if nombre_pieces is None or nombre_pieces <= 0:
        errors.append("Nombre de pièces doit être > 0.")
    if not code_postal or len(code_postal) != 5 or not code_postal.isdigit():
        errors.append("Code postal invalide (5 chiffres).")
    if not commune:
        errors.append("Commune introuvable — renseignez manuellement la commune.")
    if len(errors) > 0:
        for e in errors:
            st.error(e)
        st.stop()

    # géocodage (lat/lon)
    lat, lon = geocode_address(numero or "0", rue or "", code_postal, commune)
    if lat is None or lon is None:
        st.warning("Géocodage impossible → tentative avec le centre de la commune via API Gouv")
        # fallback: use geo.api.gouv.fr to get centroid? we use None-check and stop if absent
        # try to get approximate centroid by calling the geo API (not always available)
        try:
            url = f"https://geo.api.gouv.fr/communes?codePostal={code_postal}&fields=centre&format=json"
            r = requests.get(url, timeout=4).json()
            if r and "centre" in r[0]:
                centre = r[0]["centre"]
                lat = centre["coordinates"][1]
                lon = centre["coordinates"][0]
                st.info("Coordonnées approximatives (centre commune) utilisées.")
        except Exception:
            pass

    if lat is None or lon is None:
        st.error("Impossible d'obtenir latitude/longitude. Vérifiez adresse / commune.")
        st.stop()

    # construire DataFrame pour le pipeline — types stricts
    X_input = pd.DataFrame([{
        "surface_utilisee": float(surface_habitable),
        "surface_terrain": float(surface_terrain) if surface_terrain is not None else 0.0,
        "nombre_pieces_principales": int(nombre_pieces),
        "latitude": float(lat),
        "longitude": float(lon),
        "code_postal": str(code_postal),
        "code_commune": str(code_commune) if code_commune is not None else str(""),
        "code_departement": str(code_departement) if code_departement is not None else str(code_postal[:2])
    }])

    # debug lines (commenter en prod)
    # st.write("Input envoyé au modèle :"); st.write(X_input); st.write(X_input.dtypes)

    # sélectionner modèle
    model = models["maison"] if type_bien.lower().startswith("maison") else models["appart"]
    if model is None:
        st.error("Modèle pour ce type non disponible (erreur de chargement).")
        st.stop()

    try:
        pred_log = model.predict(X_input)
        prix = float(np.expm1(pred_log[0]))  # reconvertir log1p -> euros
        st.success(f"Prix estimé : {prix:,.0f} €")
        st.info(f"Fourchette indicative: {prix*0.9:,.0f} € — {prix*1.1:,.0f} €")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
        st.exception(e)
        st.write("Input envoyé au modèle (pour debug):")
        st.write(X_input)
