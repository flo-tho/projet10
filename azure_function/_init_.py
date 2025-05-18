import logging
import azure.functions as func
import pandas as pd
import json
from recommender import ContentBasedRecommender
import os

# Chargement en mémoire du modèle (au cold start uniquement)
article_features = pd.read_pickle(os.path.join(os.path.dirname(__file__), 'article_features.pkl'))
recommender = ContentBasedRecommender(article_features)

# Simule une base utilisateur (à remplacer par appel BDD plus tard)
with open(os.path.join(os.path.dirname(__file__), 'user_history.json')) as f:
    USER_HISTORY = json.load(f)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function called for recommendations.')

    user_id = req.params.get('user_id')
    if not user_id:
        return func.HttpResponse("Missing user_id", status_code=400)

    user_history = USER_HISTORY.get(user_id)
    if not user_history:
        return func.HttpResponse("Unknown user or empty history", status_code=404)

    recommendations = recommender.recommend_items(
        user_id=user_id,
        user_history=user_history,
        topn=5
    )

    return func.HttpResponse(recommendations.to_json(orient="records"), mimetype="application/json")
