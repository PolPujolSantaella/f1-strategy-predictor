import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_drivers, get_driver_stats
from src.url_images import get_image_from_wikipedia
from src.visualizations import plot_evolution_points_season

def display_comparation_section():
    st.markdown("## 🆚 Compare")
    
    df = load_drivers()
    pilots = sorted(df["driverRef"].dropna().unique())
    
    pilots_upper = [p.upper() for p in pilots]
    
    col1, col2 = st.columns(2)
    with col1:
        pilot1 = st.selectbox("Select Driver: ", pilots_upper, key="pilot_1")
        pilot1 = pilot1.lower()
    with col2:
        pilot2 = st.selectbox("Select Driver: ", pilots_upper, key="pilot_2")
        pilot2 = pilot2.lower()
        
        
    if pilot1 and pilot2 and pilot1 != pilot2:
        
        season1, _, _, info1 = get_driver_stats(pilot1)
        season2, _, _, info2 = get_driver_stats(pilot2)
        
        if season1 is None or season2 is None:
            st.warning("Data no available for one of the drivers")
            return
        
        def resume(stats):
            total_races = stats['races'].sum()
            total_wins = stats['wins'].sum()
            total_poles = stats['poles'].sum()
            total_podiums = stats['podiums'].sum()
            avg_position = stats['wins'].sum() / stats['races'].sum() if stats['races'].sum() > 0 else 0
            total_points = stats['points'].sum()
            return {
                'Races': total_races,
                'Wins': total_wins,
                'Poles': total_poles,
                'Podiums': total_podiums,
                'Points': total_points,
                'Avg Win Rate': avg_position * 100,
            }
            
        resume1 = resume(season1)
        resume2 = resume(season2)
        
        col1, col2, col3 = st.columns([4, 2, 4])
        with col1:
            img1 = get_image_from_wikipedia(info1['url'])
            st.image(img1, caption=f"{info1['forename']} {info1['surname']}", use_container_width =True)
        with col2:
             st.markdown("<h1 style='text-align:center; margin-top: 100px;'>VS</h1>", unsafe_allow_html=True)
        with col3:
            img2 = get_image_from_wikipedia(info2['url'])
            st.image(img2, caption=f"{info2['forename']} {info2['surname']}", use_container_width=True)
            
        st.markdown("<h3 style='text-align: center;'>📊 Key Metrics Comparison</h3>", unsafe_allow_html=True)
        
        for metric in resume1.keys():
            val1 = resume1[metric]
            val2 = resume2[metric]
            
            val1_fmt = f"{val1:.1f}" if isinstance(val1, float) else f"{int(val1)}"
            val2_fmt = f"{val2:.1f}" if isinstance(val2, float) else f"{int(val2)}"

            col1, col2, col3 = st.columns([4, 2, 4])
            with col1:
                color = "green" if val1 > val2 else "white"
                st.markdown(f"<div style='color:{color}; text-align:center; font-weight:bold'>{val1_fmt}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='text-align:center;'>{metric}</div>", unsafe_allow_html=True)
            with col3:
                color = "green" if val2 > val1 else "white"
                st.markdown(f"<div style='color:{color}; text-align:center; font-weight:bold'>{val2_fmt}</div>", unsafe_allow_html=True)

        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Evolution of Points", 
            "📊 Key Metrics Bar Chart", 
            "🎯 Positions Overview", 
            "📉 Avg Points per Season"
        ]) 
        with tab1:
            st.markdown("#### Evolution of Points by Season")
            fig_season = plot_evolution_points_season(season1, season2, pilot1, pilot2)
            st.plotly_chart(fig_season, use_container_width=True)
        