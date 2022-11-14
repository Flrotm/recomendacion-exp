import streamlit as st
import streamlit_analytics
from caminoa import show_camino_a
from caminob import show_camino_b
import os


def main():
    os.makedirs("stats", exist_ok=True)
    # type: ignore
    with streamlit_analytics.track(save_to_json="stats/stats.json", load_from_json="stats/stats.json"):
        page = st.sidebar.selectbox(
            "Experimento", ("Experimento A", "Experimento B", "Estadisticas"))

        if page == "Experimento A":
            st.experimental_set_query_params(analytics="off")
            show_camino_a()
        elif page == "Experimento B":
            st.experimental_set_query_params(analytics="off")
            show_camino_b()
        else:
            st.experimental_set_query_params(analytics="on")


if __name__ == "__main__":
    main()
