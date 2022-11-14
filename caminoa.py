import numpy as np
import streamlit as st
from model import generate_recommendations, get_movie_data_by_id

countries = (
    "Perú",
    "Argentina",
    "Chile",
    "Colombia",
    "Ecuador",
    "España",
    "México",
    "Venezuela",
    "Estados Unidos",
    "Otro"
)

education = (
    "Hombre",
    "Mujer",
    "Otro",
)


def display_movie_with_id(id: int):
    movie_data = get_movie_data_by_id(id)
    if movie_data is None:
        return False

    title, categories, image_1, overview_1 = movie_data

    col1, col2 = st.columns(2)
    col1.write("**" + title + "**")
    col1.write("Categorias:  " + categories)
    col1.write("Trama:  " + str(overview_1))
    col2.image(image_1, width=250)
    return True


def show_camino_a():
    st.title("Experimento A")
    st.write("""Disclaimer: Toda la información utilizada en este experimento es anónima y se respeta la confidencialidad de los usuarios. El propósito de este experimento es parte de una investigación en ciencia de la computación. """)
    st.write("""En este experimento, primero se solicita información personal, luego se pide un rating
    inicial de un grupo de películas, se muestran las recomendaciones y finalmente se pide una evaluación de estas recomendaciones""")
    st.write("""### Información personal""")

    # unused variables momento
    selected_country = st.selectbox("País", countries)
    selected_education = st.selectbox("Genero", education)
    selected_age = st.slider("Edad", 15, 65, 25)

    st.write("""## Rating Inicial""")
    st.write(""" Por favor evalue las siguientes peliculas con un rating del 1 a 5, donde 1 es el mínimo y 5 es el más positivo. En caso no haya visto la película, tome en cuenta qué tan probable es que la vea según la información disponible.""")

    shown_movies_ids = [72998, 202439, 1, 103075, 179595]

    shown_movies_ratings = []
    for movie_id in shown_movies_ids:
        display_movie_with_id(movie_id)
        rating = st.slider("Rating", 1, 5, 3, key=movie_id)
        shown_movies_ratings.append(rating)

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0099ff;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #00ff00;
        color:#ff0000;
        }
    </style>""", unsafe_allow_html=True)
    st.write(""" A continuación presione el botón para generar las recomendaciones.  Esto toma unos segundos""")
    ok = st.button("Generar recomendaciones ")
    if ok:
        with st.spinner('Generando recomendaciones...'):
            user_ratings = np.array(shown_movies_ratings)
            movies_ids = np.array(shown_movies_ids)
            titles = generate_recommendations(user_ratings, movies_ids)

            for i in titles.index:
                success = display_movie_with_id(i)
                if not success:
                    display_movie_with_id(208038)  # why

            st.markdown(
                "## Por favor pase a la sección B del experimento en la parte izquierda")
