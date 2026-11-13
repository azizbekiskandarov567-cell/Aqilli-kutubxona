"""Gibrid tavsiya moduli: content-based (TF-IDF) + item-item collaborative filtering."""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationService:
    def __init__(self, books: pd.DataFrame, ratings: pd.DataFrame):
        # books: id, title, description, category, authors
        # ratings: user_id, book_id, value
        self.books = books.reset_index(drop=True)
        self.ratings = ratings
        text = (self.books["title"].fillna("") + " " +
                self.books["description"].fillna("") + " " +
                self.books["category"].fillna("") + " " +
                self.books["authors"].fillna(""))
        tfidf = TfidfVectorizer(max_features=5000)
        self.content_sim = cosine_similarity(tfidf.fit_transform(text))
        self.ids = self.books["id"].tolist()
        self.index = {b: i for i, b in enumerate(self.ids)}
        matrix = ratings.pivot_table(index="user_id", columns="book_id",
                                     values="value", fill_value=0)
        self.matrix = matrix.reindex(columns=self.ids, fill_value=0)
        self.collab_sim = cosine_similarity(self.matrix.T.values) if len(self.matrix) else None

    def recommend(self, user_id, n=10, w_content=0.5, w_collab=0.5):
        if user_id not in self.matrix.index:
            return self.popular(n)  # cold start
        user_vec = self.matrix.loc[user_id].values
        seen = user_vec > 0
        collab = self.collab_sim.dot(user_vec)
        content = self.content_sim.dot(user_vec)
        score = w_content * self._norm(content) + w_collab * self._norm(collab)
        score[seen] = -1  # o'qilgan kitoblarni chiqarmaymiz
        top = np.argsort(score)[::-1][:n]
        return [(self.ids[i], float(score[i])) for i in top]

    def popular(self, n=10):
        pop = self.ratings.groupby("book_id")["value"].sum().sort_values(ascending=False)
        return [(int(b), float(s)) for b, s in pop.head(n).items()]

    @staticmethod
    def _norm(x):
        m = x.max()
        return x / m if m > 0 else x
