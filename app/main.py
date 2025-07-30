import streamlit as st 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.visualizations import plot_driver_stats

st.set_page_config(page_title="F1 Dashboard", layout="wide")

df = load_data()

st.title("🏎️ F1 Dashboard - Historia y Predicción")
st.markdown("Explora los datos históricos de la Fórmula 1 desde 1950 hasta 2020. Analiza pilotos, equipos, circuitos y predice resultados.")

# Inyectar CSS para el sidebar
st.markdown("""
    <style>
    /* Centrar contenido del sidebar */
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 10px;
    }

    /* Título del sidebar más grande */
    .sidebar-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Botones/radio más grandes */
    .css-1cpxqw2, .css-1d391kg {
        font-size: 30px !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("img/f1_logo.jpg", width=150)


# Sidebar estilizado
st.sidebar.markdown('<div class="sidebar-title">Analysis</div>', unsafe_allow_html=True)


# Menú con iconos y texto centrado
option = st.sidebar.radio("",
    ["📍 Circuits", "🏁 Pilots", "📅 Races"]
)

if option == "🏁 Pilots":
    st.title("Driver Statistics")
elif option == "📍 Circuits":
    st.title("Circuit Statistics")
elif option == "📅 Races":
    st.title("Race Statistics")
