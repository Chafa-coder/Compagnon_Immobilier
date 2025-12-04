import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ----------------------------
#   PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="4 - Modélisation du Prix",
    layout="wide"
)

st.title("Comparaison des Modèles — Détection d'Overfitting")

# ----------------------------
#            DATA
# ----------------------------
# csv_path = r"C:\Users\cbent\Projets\data\outputs_modelisation\model_comparison_stable.csv"
csv_path = Path("data") / "outputs_modelisation" / "model_comparison_stable.csv"

try:
    df = pd.read_csv(csv_path)
    # st.success("Fichier chargé avec succès !")
except Exception as e:
    st.error(f"Erreur lors du chargement du CSV : {e}")
    st.stop()

st.subheader("Données du fichier")
st.dataframe(df, use_container_width=True)


# ----------------------------
#   BEST MODEL SELECTION (NEW)
# ----------------------------

# Nouveau score équilibré : bonne perf + peu d'overfitting
df["model_score"] = (
    df["MAE_test"]
    * (1 + df["ΔR2"] + df["ΔMAE(%)"] / 100)
)

best_idx = df["model_score"].idxmin()
best_model = df.loc[best_idx, "Model"]

st.success(f"Meilleur modèle (performance + faible overfitting) : **{best_model}**")

# ----------------------------
#   GRAPH: MAE Train vs Test
# ----------------------------

st.subheader("Détection d'Overfitting : MAE Train vs MAE Test")

fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(df["MAE_train"], df["MAE_test"], s=200)

for i, row in df.iterrows():
    ax.text(
        row["MAE_train"] * 1.01,
        row["MAE_test"] * 1.01,
        row["Model"],
        fontsize=12
    )

min_mae = min(df["MAE_train"].min(), df["MAE_test"].min())
max_mae = max(df["MAE_train"].max(), df["MAE_test"].max())
ax.plot([min_mae, max_mae], [min_mae, max_mae], "--", color="gray")

# Annotation du meilleur modèle
bm = df.loc[best_idx]
ax.annotate(
    f"Meilleur compromis puissance-généralisation)",
    xy=(bm["MAE_train"], bm["MAE_test"]),
    xytext=(bm["MAE_train"] * 1.12, bm["MAE_test"] * 0.9),
    arrowprops=dict(arrowstyle='->', lw=2),
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
)

ax.set_title("Comparaison MAE Train vs Test — Détection d'Overfitting", fontsize=16)
ax.set_xlabel("MAE Train", fontsize=14)
ax.set_ylabel("MAE Test", fontsize=14)
ax.grid(True, alpha=0.3)

st.pyplot(fig)

    
st.title("Meilleur modèle appliqué sur type de bien")

# ----------------------------
#            DATA
# ----------------------------
# csv_path = r"C:\Users\cbent\Projets\data\outputs_modelisation\comparaison_modeles.csv"
csv_path = Path("data") / "outputs_modelisation" / "comparaison_modeles.csv"

try:
    df_ma = pd.read_csv(csv_path)
    st.success("Fichier chargé avec succès !")
except Exception as e:
    st.error(f"Erreur lors du chargement du CSV : {e}")
    st.stop()

st.subheader("Données du fichier")
st.dataframe(df_ma, use_container_width=True)



# ---- CONFIG ----
st.set_page_config(page_title="Modélisation Prix Immo", layout="wide")
# output_dir = r"C:\Users\cbent\Projets\data\outputs_modelisation"
output_dir = Path("data") / "outputs_modelisation"


# ---- SECTION 4 : FICHIERS SHAP ----
st.subheader("Interprétations SHAP")
col1, col2 = st.columns(2)
col1.image(os.path.join(output_dir, "shap_maison.png"), caption="SHAP Maisons", use_container_width=True)
col2.image(os.path.join(output_dir, "shap_appartement.png"), caption="SHAP Appartements", use_container_width=True)

# ---- FOOTER ----
st.markdown("---")
st.caption("Données préparées sous Jupyter | Interface Streamlit pour la visualisation")
