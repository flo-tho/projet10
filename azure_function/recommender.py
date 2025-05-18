class ContentBasedRecommender:
    def __init__(self, article_features: pd.DataFrame):
        """
        article_features: DataFrame indexé par article_id, colonnes = features
        """
        # Pré-calcul de la matrice de similarité article-article
        self.article_features = article_features
        self.article_ids = article_features.index.tolist()
        self.similarity_matrix = pd.DataFrame(
            cosine_similarity(article_features),
            index=self.article_ids,
            columns=self.article_ids
        )

    def get_model_name(self):
        return "ContentBasedRecommender"

    def recommend_items(self, user_id, items_to_ignore=None, topn=10, user_history=None):
        if user_history is None or len(user_history) == 0:
            return pd.DataFrame(columns=['click_article_id', 'score'])

        # Normalisation des types d’IDs
        user_history = [int(i) for i in user_history]
        if items_to_ignore:
            items_to_ignore = [int(i) for i in items_to_ignore]

        # Agrégation des similarités
        similar_scores = self.similarity_matrix.loc[user_history].mean(axis=0)

        # if items_to_ignore:
        #     similar_scores = similar_scores.drop(index=items_to_ignore, errors='ignore')

        top_recs = similar_scores.sort_values(ascending=False).head(topn)

        return pd.DataFrame({
            'click_article_id': top_recs.index.astype(int),
            'score': top_recs.values
        })