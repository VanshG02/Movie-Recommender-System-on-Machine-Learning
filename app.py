import streamlit as st
import pickle
import requests
import pandas as pd


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key='
                            '8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500" + data['poster_path']
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_names = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.header('Movie Recommender System')
movie_list = movies['title'].values

selected_movie_name = st.selectbox('FIND A MOVIE OF YOUR CHOICE BELOW?',
                                   movie_list)

if st.button('Recommend'):
    recommended_names, recommended_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_names[0])
        st.image(recommended_posters[0])
    with col2:
        st.text(recommended_names[1])
        st.image(recommended_posters[1])
    with col3:
        st.text(recommended_names[2])
        st.image(recommended_posters[2])
    with col4:
        st.text(recommended_names[3])
        st.image(recommended_posters[3])
    with col5:
        st.text(recommended_names[4])
        st.image(recommended_posters[4])
