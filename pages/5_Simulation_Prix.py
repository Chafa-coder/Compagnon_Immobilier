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
    st.success("**Saisir les informations sur le bien**")
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
        # geolocator = Nominatim(user_agent="estimation_app")
        geolocator = Nominatim(user_agent="estimation_immo_app_contact@votreadresse.com")
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
    # --- Saisie CP ---
    code_postal = st.text_input("Code postal", value="", key="code_postal")

    # --- Initialisation safe des variables dans session_state ---
    if "commune_detectee" not in st.session_state:
        st.session_state["commune_detectee"] = ""
    if "code_commune" not in st.session_state:
        st.session_state["code_commune"] = ""
    if "code_departement" not in st.session_state:
        st.session_state["code_departement"] = ""

    # --- Appel automatique API suivant code postal ---
    if (
        st.session_state.code_postal
        and len(st.session_state.code_postal) == 5
        and st.session_state.code_postal.isdigit()
    ):
        c, cc, cd = get_commune_from_cp(st.session_state.code_postal)

        if c:  # Mise à jour de la commune détectée
            st.session_state.commune_detectee = c
            st.session_state.code_commune = cc
            st.session_state.code_departement = cd
        else:
            st.session_state.commune_detectee = ""
            st.session_state.code_commune = ""
            st.session_state.code_departement = ""

    # --- Affichage du champ Commune (lecture seule) ---
    st.text_input(
        "Commune détectée",
        value=st.session_state.commune_detectee,
        disabled=True
    )

# On expose commune / code_commune / code_departement comme variables locales utilisables plus loin
commune = st.session_state.commune_detectee
code_commune = st.session_state.code_commune
code_departement = st.session_state.code_departement


        
col_left, col_right = st.columns([2,1])

with col_left:
    # st.subheader("Caractéristiques du bien")
    type_bien = st.selectbox("Type de bien", ["Maison", "Appartement"])
    # surface_habitable = st.number_input("Surface habitable (m²)", min_value=1.0, value=50.0, step=1.0)
    surface_habitable_str = st.text_input("Surface habitable (m²)", value="50")
    try:
        surface_habitable = float(surface_habitable_str)
    except ValueError:
        surface_habitable = None  # Indique une saisie invalide
    
with col_right:
    nombre_pieces = st.number_input("Nombre de pièces", min_value=1, value=3, step=1)
    surface_terrain = 0.0
    if type_bien == "Maison":
        surface_terrain = st.number_input("Surface terrain (m²)", min_value=0.0, value=0.0, step=1.0)


# -----------------------
# Bouton prédiction
# -----------------------
if st.button("Estimer le prix"):

    # validations explicites
    errors = []
    if surface_habitable is None or surface_habitable <= 0:
        errors.append("Surface habitable doit être numérique > 0.")
    if nombre_pieces is None or nombre_pieces <= 0:
        errors.append("Nombre de pièces doit être > 0.")
    if not code_postal or len(code_postal) != 5 or not code_postal.isdigit():
        errors.append("Code postal invalide (5 chiffres).")
    if not commune:
        errors.append("Code postal introuvable")
    if len(errors) > 0:
        for e in errors:
            st.error(e)
        st.stop()
    
    errors = []
    if not rue or len(rue.strip()) < 3:
        errors.append("Le nom de la rue est obligatoire et doit être complet (ex: 'avenue de la République').")
    if not numero or len(numero.strip()) < 1:
        errors.append("Le numéro de la rue est obligatoire.")
    if len(errors) > 0:
        for e in errors:
            st.error(e)
        st.stop()


    # Géocodage strict de l’adresse
    lat, lon = geocode_address(numero or "0", rue or "", code_postal, commune)
    if lat is None or lon is None:
        st.error(
            "Géocodage impossible : vérifiez que le numéro, le nom de la rue, "
            "le code postal et la commune sont corrects."
            )
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
        st.success(f"Prix estimé : {prix:,.0f} €".replace(",", " "))
        # st.success(f"Prix estimé : {prix:,.0f} €")
        # st.info(f"Fourchette indicative: {prix*0.9:,.0f} € — {prix*1.1:,.0f} €")
        st.info(f"Fourchette indicative: {prix*0.9:,.0f} € — {prix*1.1:,.0f} €".replace(",", " "))
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
        st.exception(e)
        st.write("Input envoyé au modèle (pour debug):")
        st.write(X_input)
