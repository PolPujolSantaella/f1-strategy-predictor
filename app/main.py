import streamlit as st 
import pandas as pd
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_drivers, load_circuits, get_driver_stats
from src.url_images import pilot_images, get_image_from_wikipedia
from src.visualizations import (
                                plot_driver_stats,
                                plot_position_distribution,
                                plot_circuit_performance
                                )


st.set_page_config(page_title="F1 Dashboard", layout="wide")


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
    df = load_drivers()
    pilots = sorted(df["surname"].dropna().unique())
    pilot_selected = st.selectbox("Select a driver", pilots)
    
    if pilot_selected:
        st.subheader(f"{pilot_selected}")
        
        wiki_url = df.loc[df["surname"] == pilot_selected, "url"].values[0]
        img_url = get_image_from_wikipedia(wiki_url)
        
        if img_url:
            st.image(img_url, width=250, caption=pilot_selected)
        else:
            st.info("No image available for this driver in Wikipedia.")
        
    else:
        st.info("No image available for this driver.")
    
    
    pilot_data = df[df['surname'] == pilot_selected].iloc[0]
    
    st.markdown(f"""
                **Name:** {pilot_data['forename']} {pilot_data['surname']}  
                **Number:** {pilot_data['number'] if pd.notna(pilot_data['number']) else 'N/A'}  
                **Date of Birth:** {pilot_data['dob']}  
                **Nationality:** {pilot_data['nationality']}  
                """)
    
    season_summary, position_dist, circuit_stats, _ = get_driver_stats(pilot_selected)
    
    if season_summary is None:
        st.warning("No data available for this driver.")
    else:
        st.markdown("---")
        st.subheader("Season Evolution")
        fig_season = plot_driver_stats(season_summary, pilot_selected)
        st.plotly_chart(fig_season, use_container_width=True)
        
        st.subheader("Position Distribution")
        fig_position = plot_position_distribution(position_dist, pilot_selected)
        st.plotly_chart(fig_position, use_container_width=True)
        
        st.subheader("Circuit Performance")
        fig_circuit = plot_circuit_performance(circuit_stats, pilot_selected)
        st.plotly_chart(fig_circuit, use_container_width=True)
        
    
    
elif option == "📍 Circuits":
    st.title("Circuit Statistics")
    df = load_circuits()
    circuits = sorted(df["name"].dropna().unique())
    circuit_selected = st.selectbox("Select a circuit", circuits)

elif option == "📅 Races":
    st.title("Race Statistics")
