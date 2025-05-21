import streamlit as st
import requests
import pandas as pd
import json

# URL de la fonction Azure
AZURE_FUNCTION_URL = "https://articlesrecommender.azurewebsites.net/api/recommender"
# AZURE_FUNCTION_URL = "http://localhost:7071/api/recommender"

# Charger dynamiquement les user_ids depuis le fichier JSON
@st.cache_data
def load_user_ids(json_path="azure_function/user_history.json"):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        user_ids = sorted(map(int, data.keys()))
        return user_ids
    except Exception as e:
        st.error(f"Erreur lors du chargement de user_history.json : {e}")
        return []

st.set_page_config(page_title="Recommandation d'articles", layout="centered")

st.title("Recommandation d'articles")
st.markdown("Sélectionnez un utilisateur pour obtenir des recommandations personnalisées.")

# Charger les IDs d'utilisateurs
user_ids = load_user_ids()

if user_ids:
    user_id = st.selectbox("Sélectionnez un utilisateur :", user_ids)

    if st.button("Obtenir les recommandations"):
        with st.spinner("Chargement..."):
            try:
                response = requests.get(AZURE_FUNCTION_URL, params={"user_id": user_id})
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data)
                    df.columns = ["ID de l'article", "Score de pertinence"]
                    st.success("Recommandations obtenues :")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error(f"Erreur {response.status_code} : {response.text}")
            except Exception as e:
                st.error(f"Erreur de connexion à l'API : {e}")
else:
    st.warning("Aucun utilisateur trouvé dans le fichier user_history.json.")


# import streamlit as st
# import requests
# import pandas as pd
#
# # URL de la fonction Azure (modifie si déployée en ligne)
# AZURE_FUNCTION_URL = "http://localhost:7071/api/recommender"
#
# # Liste statique des user_ids à sélectionner
# USER_IDS = [1076,  1465, 16081, 93849, 13231,  4837, 59193, 45061, 44812, 43369]
#
# st.set_page_config(page_title="Recommandation d'articles", layout="centered")
#
# st.title("Recommandation d'articles")
# st.markdown("Sélectionnez un utilisateur pour obtenir les recommandations personnalisées.")
#
# # Sélecteur dropdown pour user_id
# user_id = st.selectbox("Sélectionnez un utilisateur :", USER_IDS)
#
# # Bouton pour lancer la requête
# if st.button("Obtenir les recommandations"):
#     with st.spinner("Chargement..."):
#         try:
#             response = requests.get(AZURE_FUNCTION_URL, params={"user_id": user_id})
#             if response.status_code == 200:
#                 data = response.json()
#                 df = pd.DataFrame(data)
#                 df.columns = ["ID de l'article", "Score de pertinence"]
#                 st.success("Recommandations trouvées :")
#                 st.dataframe(df, use_container_width=True)
#             else:
#                 st.error(f"Erreur {response.status_code} : {response.text}")
#         except Exception as e:
#             st.error(f"Erreur de connexion à l'API : {e}")
