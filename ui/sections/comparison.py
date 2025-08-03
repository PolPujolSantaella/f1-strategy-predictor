import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_drivers, get_driver_stats
from src.url_images import get_image_from_wikipedia
from src.visualizations import (
    plot_evolution_points_season, 
    plot_key_performance, 
    plot_final_position_distribution, 
    plot_average_points_season
)

def get_driver_summary(stats: pd.DataFrame) -> dict:
    """Compute summary metrics for a driver."""
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
    

def display_comparison_section() -> None:
    """Render the driver comparison section."""
    st.markdown("## 🆚 Compare")
    
    df = load_drivers()
    driver_refs = sorted(df["driverRef"].dropna().unique())
    driver_names = [ref.upper() for ref in driver_refs]
    
    col1, col2 = st.columns(2)
    with col1:
        driver_1 = st.selectbox("Select Driver:", driver_names, key="pilot_1").lower()
    with col2:
        driver_2 = st.selectbox("SelectDriver:", driver_names, key="pilot_2").lower()
        
    if driver_1 == driver_2:
        st.warning("Please select two differents drivers for comparison")
        return
        
    if driver_1 and driver_2:
        season1, _, _, info1 = get_driver_stats(driver_1)
        season2, _, _, info2 = get_driver_stats(driver_2)
        
        if season1 is None or season2 is None:
            st.warning("Data no available for one of the drivers")
            return
        
        summary1 = get_driver_summary(season1)
        summary2 = get_driver_summary(season2)
        
        show_driver_images(info1, info2)
        display_key_metrics(summary1, summary2)
        
        st.markdown("---")
        
        show_comparison_tabs(season1, season2, summary1, summary2, driver_1, driver_2)
        
        
def show_driver_images(info1: dict, info2: dict) -> None:
    """Show side-by-side driver images."""
    col1, col2, col3 = st.columns([4, 2, 4])
    with col1:
        img1 = get_image_from_wikipedia(info1['url'])
        st.image(img1, caption=f"{info1['forename']} {info1['surname']}", use_container_width =True)
    with col2:
        st.markdown("<h1 style='text-align:center; margin-top: 150px;'>VS</h1>", unsafe_allow_html=True)
    with col3:
        img2 = get_image_from_wikipedia(info2['url'])
        st.image(img2, caption=f"{info2['forename']} {info2['surname']}", use_container_width=True)
        
def display_key_metrics(summary1: dict, summary2: dict) -> None:
    """Render the key metrics comparison."""    
    st.markdown("<h3 style='text-align: center;'>📊 Key Metrics Comparison</h3>", unsafe_allow_html=True)
        
    for metric in summary1.keys():
        val1, val2 = summary1[metric], summary2[metric]
        
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


def show_comparison_tabs(season1, season2, summary1, summary2, driver_1: str, driver_2: str) -> None:
    """Display visual comparison tabs for both drivers."""
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Evolution of Points", 
        "📊 Key Metrics Bar Chart", 
        "🎯 Positions Overview", 
        "📉 Avg Points per Season"
    ]) 
        
    with tab1:
        st.markdown("#### Evolution of Points by Season")
        fig_season = plot_evolution_points_season(season1, season2, driver_1, driver_2)
        st.plotly_chart(fig_season, use_container_width=True)
            
    with tab2:
        st.markdown("#### Key Performance Comparison")
        fig = plot_key_performance(summary1, summary2, driver_1, driver_2)
        st.plotly_chart(fig, use_container_width=True)
            
    with tab3:
        st.markdown("#### Final Positions Distribution")
        pos1 = get_position_distribution(season1)
        pos2 = get_position_distribution(season2)
        fig = plot_final_position_distribution(pos1, pos2, driver_1, driver_2)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("#### Average Points per Season")
        avg1 = season1["points"].mean()
        avg2 = season2["points"].mean()
        fig = plot_average_points_season(avg1, avg2, driver_1, driver_2)
        st.plotly_chart(fig, use_container_width=True)
        
def get_position_distribution(season_summary: pd.DataFrame) -> pd.Series:
    """Calculate simplified position categories."""
    pos_counts = season_summary[["wins", "podiums", "races"]].sum()
    pos_counts["Others"] = pos_counts["races"] - (pos_counts["wins"] + pos_counts["podiums"])
    return pos_counts[["wins", "podiums", "Others"]]
        