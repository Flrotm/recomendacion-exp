import numpy as np
import streamlit as st
from model import generate_recommendations, get_movie_data_by_id

countries_options = (
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
education_options = (
    "Hombre",
    "Mujer",
    "Otro",
)


def callback(titles):
    st.session_state.titles = titles


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


def show_camino_b():
    st.title("Experimento B")
    st.write("""Disclaimer: Toda la información utilizada en este experimento es anónima y se respeta la confidencialidad de los usuarios. El proposito de este experimento es como parte de una investigación. """)
    st.write("""En este experimento,primero se solicita información personal, luego se pide un rating
    inicial de un grupo de películas, se muestran las recomendaciones y finalmente se pide una evaluación de estas recomendaciones""")
    st.write("""### Información personal""")

    selected_country = st.selectbox("País", countries_options)
    selected_education = st.selectbox("Genero", education_options)

    selected_edad = st.slider("Edad", 15, 65, 25)

    st.write("""## Películas rating""")
    st.write(""" Por favor evalue las siguientes Películas con un rating del 1 a 5, donde 5 es el mas postivo. En caso no haya visto la Película, tome en cuenta que tan probable es que la vea segun la infromacion disponible""")

    first_movie_id = 109487
    display_movie_with_id(first_movie_id)
    b_rating = st.slider(" Película 1", 1, 5, 1)

    second_movie_id = 128360
    display_movie_with_id(128360)
    b_rating2 = st.slider(" Película 2", 1, 5, 1)

    third_movie_id = 5618
    display_movie_with_id(third_movie_id)
    b_rating3 = st.slider("Película 3", 1, 5, 1)

    fourth_movie_id = 179217
    display_movie_with_id(fourth_movie_id)
    b_rating4 = st.slider(" Película 4", 1, 5, 1)

    fifth_movie_id = 179585
    display_movie_with_id(fifth_movie_id)
    b_rating5 = st.slider(" Película 5", 1, 5, 1)

    st.write(""" A continuación presione el botón para generar las recomendaciones, puede tardar unos segundos""")
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

    ok1 = st.button("Generar recomendaciones ")

    if ok1:
        with st.spinner('Generando recomendaciones...'):
            user_ratings = np.array(
                [b_rating, b_rating2, b_rating3, b_rating4, b_rating5])
            movies_ids = np.array(
                [first_movie_id, second_movie_id, third_movie_id, fourth_movie_id, fifth_movie_id])

            titles = generate_recommendations(user_ratings, movies_ids)

            st.session_state.titles = titles.title

            j = 0
            for i in titles.index:
                if j<2:
                    st.write("Esta recomendación fue generada en base a su información personal")
                else:
                    st.write("Esta recomendación fue generada en base a su rating inicial")
                success = display_movie_with_id(i)
                if not success:
                    display_movie_with_id(208038)  # why
                j+=1

    st.write("Por favor observe las recomendaciones y presione el botón para mostrar las recomendaciones")
    try:
        st.session_state.titles
    except:
        st.session_state.titles = []
    agree = st.checkbox('Mostrar recomendación',
                        on_change=callback(st.session_state.titles))

    if agree:
        st.write(st.session_state.titles)
    rating1 = st.slider("Pelicula1", 1, 5, 1)
    rating2 = st.slider("Pelicula2", 1, 5, 1)
    rating3 = st.slider("Pelicula3", 1, 5, 1)
    rating4 = st.slider("Pelicula4", 1, 5, 1)
    rating5 = st.slider("Pelicula5", 1, 5, 1)

    raitings_s = [rating1, rating2, rating3, rating4, rating5]

    ok = st.button("Generar segundo grupo de recomendaciones ")

    if ok:
        user_ratings = np.array(raitings_s)
        movies_ids = np.array(
            [first_movie_id, second_movie_id, third_movie_id, fourth_movie_id, fifth_movie_id])

        titles = generate_recommendations(user_ratings, movies_ids)

        count = 0
        movies_to_show = []
        for i in range(0, len(raitings_s)):
            if raitings_s[i] >= 4:
                movies_to_show.append(st.session_state.titles.index[i])
                count += 1
            else:
                # index out of range 
                if st.session_state.titles.index[i] in titles.index:
                    titles.drop(st.session_state.titles.index[i], inplace=True)
        print("count: ", count)

        for i in titles.index:
            movies_to_show.append(i)
        movies_to_show = set(movies_to_show)

        for i in movies_to_show:
            success = display_movie_with_id(i)
            if not success:
                display_movie_with_id(208038)

        st.session_state.title = titles.index

    st.markdown("# Evaluación")
    st.write(
        "Una vez revisadas las recomendaciones, por favor complete el siguiente formulario")
    link = '## [Formulario](https://forms.gle/BCNeQnhf2h1guDZd9)'
    st.markdown(link, unsafe_allow_html=True)
