import streamlit as st
import pandas as pd
import pickle
import requests

st.set_page_config(page_title = "Movie Recommender")
st.title('Movie Recommender System')


def get_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYzg0NTNlMTY3OGZkODAyYTJmZmRmMGNkYmY5OGJkMSIsInN1YiI6IjY0YzU3M2JiZWVjNWI1MDBhZDAyMDY4YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.3zQqogl-YgqVpJThm1UJOXOcu7TNPcwJy42hy_Oz1Aw"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie):
    recommended_movies = []
    recommended_movies_poster = []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for movie in movies_list:
        movie_id = movies.iloc[movie[0]].id
        recommended_movies.append(movies.iloc[movie[0]].title)
        recommended_movies_poster.append(get_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('moviesdict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie = st.selectbox(
    'Choose a Movie',
    movies['title'].values)
if st.button('Recommend'):
    names, poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

