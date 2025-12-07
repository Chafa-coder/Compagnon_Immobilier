
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
# import plotly.express as px
from pathlib import Path

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------

OUTPUT_DIR = Path("data") / "outputs_modélisation_temps"

st.set_page_config(page_title="Prévision interactive prix/m²", layout="wide")
st.title("Modélisation du prix au m²")



@st.cache_data
def list_available_scopes():
    """Retourne uniquement les scopes géographiques valides : FR et DEP_XX."""
    scopes = set()

    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".csv"):
            name = f.split(".")[0]

            # supprimer préfixes
            name = name.replace("backtest_", "")
            name = name.replace("forecast_xgb_", "")
            name = name.replace("history_", "")

            # on ne garde que :
            # - FR
            # - DEP_XX (exactement 2 chiffres)
            if name == "FR":
                scopes.add(name)
            # elif name.startswith("DEP_") and len(name) == 6 and name[4:].isdigit():
            elif name.startswith("DEP_") and name[4:].isdigit():
                scopes.add(name)

    scopes = sorted(scopes, key=lambda x: (x != "FR", x))
    return scopes



@st.cache_data
def load_backtest(scope):
    fname = os.path.join(OUTPUT_DIR, f"backtest_{scope}.csv")
    if os.path.exists(fname):
        return pd.read_csv(fname)
    return None

@st.cache_data
def load_forecast(scope):
    fname = os.path.join(OUTPUT_DIR, f"forecast_xgb_{scope}.csv")
    if os.path.exists(fname):
        return pd.read_csv(fname)
    return None


@st.cache_data
def load_history(scope):
    fname = os.path.join(OUTPUT_DIR, f"history_{scope}.csv")
    if os.path.exists(fname):
        return pd.read_csv(fname)
    return None


# ---------------------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------------------
scopes = list_available_scopes()

if not scopes:
    st.warning("Aucune donnée trouvée dans OUTPUT_DIR. Exécute d'abord le pipeline.")
    st.stop()

scope = st.selectbox("Choisir un périmètre :", scopes)

# ---------------------------------------------------------------------
# BACKTEST
# ---------------------------------------------------------------------
st.subheader(f"Meilleur modèle pour {scope}")

df_res = load_backtest(scope)

if df_res is not None:
    best_model = (
        df_res.groupby("model")["MAE"]
        .mean()
        .sort_values()
        .index[0]
    )
    st.success(f"**Meilleur modèle : `{best_model}`** (selon MAE moyen)")

    scores = df_res.groupby("model")[['MAE','RMSE','SMAPE']].mean().reset_index()
    st.dataframe(scores)
else:
    st.warning("Aucun backtest trouvé.")

# ---------------------------------------------------------------------
# FORECAST + HISTORIQUE
# ---------------------------------------------------------------------
st.subheader(f"Historique et prévision XGBoost — {scope}")

fc = load_forecast(scope)
hist = load_history(scope)

if fc is None:
    st.warning("Aucune prévision trouvée.")
else:
    fig = go.Figure()

    # Historique
    if hist is not None:
        fig.add_trace(go.Scatter(
            x=hist['date'],
            y=hist['prix_m2_median'],
            mode='lines+markers',
            name='Historique'
        ))

    # Prévision
    fig.add_trace(go.Scatter(
        x=fc['date'],
        y=fc['yhat'],
        mode='lines+markers',
        name='Prévision'
    ))

    # Bornes
    fig.add_trace(go.Scatter(
        x=fc['date'],
        y=fc['lower'],
        line=dict(dash='dash'),
        name='Borne basse'
    ))
    fig.add_trace(go.Scatter(
        x=fc['date'],
        y=fc['upper'],
        line=dict(dash='dash'),
        name='Borne haute'
    ))

    fig.update_layout(title=f"Prévision prix/m² — {scope}")

    st.plotly_chart(fig, use_container_width=True)

# st.info("Affichage intégré : National + départements.")


