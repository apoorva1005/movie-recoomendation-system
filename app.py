import pickle
import streamlit as st
import requests
import gdown
import os

# ==========================
# Google Drive file IDs
# ==========================
MOVIES_FILE_ID = "1pPHqGnsj6OjIEz8F4X1d-GYGrlxQXs36"
SIMILARITY_FILE_ID = "1K5wLaND2sjqvE4A0974VoSl1OiuAkUiV"

# ==========================
# Download files if missing
# ==========================
if not os.path.exists("movies.pkl"):
    gdown.download(f"https://drive.google.com/uc?id={MOVIES_FILE_ID}", "movies.pkl", quiet=False)

if not os.path.exists("simikarity.pkl"):
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", "simikarity.pkl", quiet=False)

# ==========================
# Fetch poster from TMDB API
# ==========================
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=62dbf2577567bb2081883c17f7a6549d&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# ==========================
# Recommendation Function
# ==========================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # top 5
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# ==========================
# Streamlit UI
# ==========================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("simikarity.pkl", "rb"))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
