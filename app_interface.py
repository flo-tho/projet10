import streamlit as st
import requests
import pandas as pd

# URL de la fonction Azure (modifie si déployée en ligne)
AZURE_FUNCTION_URL = "http://localhost:7071/api/recommender"

# Liste statique des user_ids à sélectionner
USER_IDS = [1076,  1465, 16081, 93849, 13231,  4837, 59193, 45061, 44812, 43369]

st.set_page_config(page_title="Recommandation d'articles", layout="centered")

st.title("Recommandation d'articles")
st.markdown("Sélectionnez un utilisateur pour obtenir les recommandations personnalisées.")

# Sélecteur dropdown pour user_id
user_id = st.selectbox("Sélectionnez un utilisateur :", USER_IDS)

# Bouton pour lancer la requête
if st.button("Obtenir les recommandations"):
    with st.spinner("Chargement..."):
        try:
            response = requests.get(AZURE_FUNCTION_URL, params={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                df.columns = ["ID de l'article", "Score de pertinence"]
                st.success("Recommandations trouvées :")
                st.dataframe(df, use_container_width=True)
            else:
                st.error(f"Erreur {response.status_code} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
