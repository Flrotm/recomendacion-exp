import pickle
import time

import numpy as np
import pandas as pd
import requests
from recommender import EnsembleRecommender
from scipy.sparse import csr_matrix
from sklearn.decomposition._nmf import NMF


NMF_MODEL_FILE = "data/nmf_model.sav"
LINKS_FILE = "data/links.csv"
MOVIES_FILE = "data/movies.csv"
SAMPLE_FILE = "data/sample_df.csv"

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=b83c1c45fe99fda4ebe2d1089882618f&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    overview = data['overview']
    return full_path, overview


def movie_use_matrix_pivot(df_):
    mu_matrix = df_.pivot(index='userId',
                          columns='movieId',
                          values='rating').fillna(0)
    mu_matrix_cp = csr_matrix(mu_matrix.values)
    return mu_matrix, mu_matrix_cp


def get_movie_data_by_id(id):
    links_df = pd.read_csv(LINKS_FILE)
    movies_df = pd.read_csv(MOVIES_FILE)

    this_movie = movies_df[movies_df['movieId'] == id]
    if (this_movie.empty):
        return None
    title = str(this_movie["title"].values[0])
    categories = str(movies_df[movies_df["movieId"] == id]
                     ['genres'].values[0]).replace("|", ", ")
    id_tmdb = links_df[links_df["movieId"] == id]["tmdbId"].values[0]
    image_1, overview_1 = fetch_poster(id_tmdb)
    return title, categories, image_1, overview_1


def generate_recommendations(user_ratings: np.ndarray, movies_ids: np.ndarray):
    sample_df = pd.read_csv(SAMPLE_FILE)
    movies_df = pd.read_csv(MOVIES_FILE)

    rand_number = np.random.randint(0, 9)
    user_id = sample_df["userId"].value_counts().tail(10).index.tolist()[
        rand_number]
    user_ratings_df = pd.DataFrame(
        {"userId": user_id, "movieId": movies_ids, "rating": user_ratings, "timestamp": time.time()})
    user_ratings_df = user_ratings_df[[
        "userId", "movieId", "rating", "timestamp"]]

    sample_df = sample_df[sample_df["userId"] != user_id]
    print(sample_df.shape)
    sample_df = sample_df.append(user_ratings_df)
    print(sample_df.shape)

    rating_matrix, rating_matrix_cp = movie_use_matrix_pivot(sample_df)
    loaded_model: NMF = pickle.load(open(NMF_MODEL_FILE, 'rb'))

    item_vector: np.ndarray = loaded_model.components_.T
    Ensemble = EnsembleRecommender(
        sample_df, movies_df, rating_matrix, item_vector)
    titles = Ensemble.Recommend(user_id)
    return titles
