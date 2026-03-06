import streamlit as st
import pickle

movies = pickle.load(open("model/movies.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

def recommend(movie_title):
    index = movies[movies["title"] == movie_title].index[0]

    scores = []
    for i in range(len(similarity[index])):
        score = similarity[index][i]
        scores.append((i, score))

    scores.sort(key=lambda x : x[1], reverse=True)

    top5 = scores[1:6]

    titles = []
    posters = []

    for item in top5:
        titles.append(movies.iloc[item[0]].title)
        posters.append(movies.iloc[item[0]].poster)

    return titles, posters


st.title("🎬 Movie Recommender")

selected_movie = st.selectbox("Select a movie", sorted(movies["title"].values))

if st.button("Recommend"):
    titles, posters = recommend(selected_movie)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(titles[i])