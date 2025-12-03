# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 07:06:58 2025

@author: cbent
"""

import streamlit as st

st.title("🧭 6. Conclusion & perspectives")

st.markdown("""
### Synthèse
- Les **travaux préparatoires** se sont révélés déterminants pour les deux volets du projet : 
    - estimation des prix immobiliers
    - modélisation des tendances temporelles
- Modélisation du prix d’un bien immobilier :
    - les modèles linéaires ne captent pas la structure non linéaire du marché immobilier. 
    - **XGBoost** offre le meilleur équilibre entre performance et généralisation
- Modélisation de l’évolution du prix au m² (séries temporelles) : 
    - **XGBoost** est le meilleur modèle dans 4 départements sur 5
    - **ARIMA** reste une référence dans les zones où la structure temporelle est plus stable
    - **Prophet** n’a montré un réel avantage qu’à Paris
    
### Perspectives
- Enrichissement des données :
    - **Caractéristiques qualitatives** : année de construction, rénovation, étage, ascenseur,...
    - **Données socio-économiques** : emploi, revenus, fiscalité locale,...
    - **Données du quartier** : proximité transports, écoles, services, contexte urbain.
    - **Variables externes** : taux d’intérêt, évolutions réglementaires, dynamique du marché local.
- Améliorations méthodologiques :
    - Exploration de modèles de **Deep Learning** adaptés
    - Combinaison de **XGBoost + ARIMA** dans une approche ensembliste hybride
- Mise à jour **automatique** des données DVF futures
""")

st.balloons()
