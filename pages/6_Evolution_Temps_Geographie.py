import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium import Choropleth
from streamlit_folium import st_folium
from pathlib import Path

# ------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ------------------------------------------------------
st.set_page_config(
    page_title="6 - Évolution Temps & Géographie",
    layout="wide"
)

st.title("Évolution temporelle & géographique du prix par m2")

# ------------------------------------------------------
# 1. PRIX DANS LE TEMPS
# ------------------------------------------------------
st.header("Évolution du prix médian dans le temps")

# file_time = r"C:\Users\cbent\Projets\data\outputs_modélisation_temps\Agg_trim_median.csv"

file_time = Path("data") / "outputs_modélisation_temps" / "Agg_trim_median.csv"


try:
    df_time = pd.read_csv(file_time)
    df_time["trimestre"] = pd.to_datetime(df_time["trimestre"])
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier temporel : {e}")
    st.stop()


fig_time = px.line(
    df_time,
    x="trimestre",
    y="prix_m2",
    # title="Prix médian au m² dans le temps",
    markers=True
    )
fig_time.update_layout(
    xaxis_title="Trimestre",
    yaxis_title="Prix médian (€/m²)",
    hovermode="x unified"
    )
st.plotly_chart(fig_time, use_container_width=True)

# ------------------------------------------------------
# 2. PRIX PAR DÉPARTEMENT
# ------------------------------------------------------
st.header("Prix médian par département")

# file_geo = r"C:\Users\cbent\Projets\data\outputs_modélisation_temps\prix_m2_median_dept.csv"
file_geo = Path("data") / "outputs_modélisation_temps" / "prix_m2_median_dept.csv"

try:
    df_geo = pd.read_csv(file_geo)
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier géographique : {e}")
    st.stop()

# Télécharger GEOJSON officiel des départements
geojson_dept = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"

# st.write("Carte interactive des prix médians (€/m²) par département")

# Carte Folium centrée sur la France
m = folium.Map(location=[46.6, 2.4], zoom_start=6, tiles="cartodbpositron")

# Choropleth
Choropleth(
    geo_data=geojson_dept,
    data=df_geo,
    columns=("code_departement", "prix_m2_median"),
    key_on="feature.properties.code",
    fill_color="YlOrRd",
    nan_fill_color="white",
    fill_opacity=0.8,
    line_opacity=0.2,
    legend_name="Prix moyen au m² (€)"
).add_to(m)

# Ajouter info popup
for _, row in df_geo.iterrows():
    folium.Marker(
        location=[46.6, 2.4],  # position approximative remplacée par centroid si nécessaire
        popup=f"Département {row['code_departement']}<br>Prix moyen : {row['prix_m2_median']:.0f} €<br>Mutations : {row['n_mutations']:,}",
        icon=folium.Icon(color="blue", icon="info-sign")
    )

# Affichage Streamlit
st_folium(m, width=1200, height=650)

# # Tableau brut optionnel
# with st.expander("📁 Voir les données brutes par département"):
#     st.dataframe(df_geo, use_container_width=True)
