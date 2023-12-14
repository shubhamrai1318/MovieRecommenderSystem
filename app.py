import streamlit as st
import requests
import joblib
import gdown
import os

# Function to download the file from Google Drive
def download_file_from_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
    else:
        st.error(f"Failed to download file. Status Code: {response.status_code}")

# Specify the Google Drive file IDs
movies_drive_file_id = "https://drive.google.com/file/d/1x06lLB1_k-8Nt-ciWlq60qI0_kd_zBAD/view?usp=sharing"
similarity_drive_file_id = "https://drive.google.com/file/d/1DUrNc3xt4PgqnTFdZWOc6W_NP-pvKn9o/view?usp=sharing"

# Download the movies_list.pkl and similarity.pkl files
if not os.path.isfile("movies_list.pkl"):
    download_file_from_drive(movies_drive_file_id, "movies_list.pkl")

if not os.path.isfile("similarity.pkl"):
    download_file_from_drive(similarity_drive_file_id, "similarity.pkl")

# Load the movies_list.pkl file
movies = joblib.load("movies_list.pkl")
similarity = joblib.load("similarity.pkl")
movies_list = movies['title'].values

st.header("Movie Recommender System")
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4b89c243b4e6d33055e7dea9262db468&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
