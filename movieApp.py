import streamlit as st
import pickle
import pandas as pd
import requests  

# Methods



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e3fdf6b8dc0b5d36c54072dff4f11c5b&language=en-US'.format(movie_id))
    data = response.json()  # Fix: add parentheses to call the function
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movie_indices:
        movie_id = movies_df.iloc[i[0]].movie_id
        
        recommended_movies.append(movies_df.iloc[i[0]].title)
        
        # Fetching poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



# Loading dataframe of movies and similarities
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_df = pickle.load(open('movies.pkl', 'rb'))

# Body
st.title('Movie Recommender')

movie_choice = st.selectbox('Choose a movie:', movies_df['title'].values)

if st.button('Recommend'):
    names, posters = recommend(movie_choice)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
