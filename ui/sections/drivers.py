import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_drivers, get_driver_stats
from src.url_images import get_image_from_wikipedia
from src.visualizations import (
    plot_driver_stats,
    plot_position_distribution,
    plot_circuit_performance
)


def display_driver_section() -> None:
    """Display the individual driver statistics section."""
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Select Driver")
    
    try:
        df = load_drivers()
        drivers = sorted(df["driverRef"].dropna().unique())
        drivers_upper = [d.upper() for d in drivers]
        
        selected_driver = st.selectbox(
            "Select a driver for statistics:",
            drivers_upper,
            key="driver_select"
        ).lower()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_driver:
            driver_data = df[df['driverRef'] == selected_driver].iloc[0]
            
            show_driver_info(driver_data)
            
            with st.spinner(f"Loading stats for {selected_driver}..."):
                season_summary, position_dist, circuit_stats, _ = get_driver_stats(selected_driver)
                
            if season_summary is None or season_summary.empty:
                st.warning("No data available for this driver.")
                return
            
            display_driver_metrics(season_summary)
            
            display_driver_charts(season_summary, position_dist, circuit_stats, selected_driver)
        
    except (KeyError, ValueError, IndexError) as e:
        st.error(f"Error loading driver data: {str(e)}")
        

def show_driver_info(driver_data: pd.Series) -> None:
    """Show driver image and personal information side by side."""
    col1, col2 = st.columns(2)
    with col1:
        wiki_url = driver_data.get("url", "")
        if wiki_url:
            img_url = get_image_from_wikipedia(wiki_url)
            if img_url:
                st.markdown(f"""
                    <div style="height:100%; display:flex; align-items:center; justify-content:center;">
                        <img src="{img_url}" alt="Driver image"
                         style="max-height:100%; max-width:100%; border-radius:12px; object-fit:contain;" />
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Image not available.")
        else:
            st.info("Image not available.")
            
    with col2:
        st.markdown(f"""
        <div class="driver-info">
            <div class="driver-name">{driver_data['forename']} {driver_data['surname']}</div>
            <div class="driver-details">
                <div class="detail-item">
                    <div class="detail-label">Number</div>
                    <div class="detail-value">{driver_data['number'] if pd.notna(driver_data['number']) else 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Date of Birth</div>
                    <div class="detail-value">{driver_data['dob']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Nationality</div>
                    <div class="detail-value">{driver_data['nationality']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_driver_metrics(season_summary: pd.DataFrame) -> None:
    """Show basic metrics like races, wins, podiums, win rate."""
    if season_summary is None or season_summary.empty:
        return
    
    total_races = season_summary['races'].sum()
    total_wins = season_summary['wins'].sum()
    total_podiums = season_summary['podiums'].sum()
    win_rate = (total_wins / total_races * 100) if total_races > 0 else 0
        
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-box">
                <span class="metric-number">{total_races}</span>
                <span class="metric-label">Races</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{total_wins}</span>
                <span class="metric-label">Victories</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{total_podiums}</span>
                <span class="metric-label">Podiums</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{win_rate:.1f}%</span>
                <span class="metric-label">% Win Rate</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )       
    
def display_driver_charts(
    season_summary: pd.DataFrame,
    position_dist: pd.DataFrame,
    circuit_stats: pd.DataFrame,
    driver_id: str
) -> None:
    """Show driver graphs accross 3 main tabs."""
    tab1, tab2, tab3 = st.tabs([
        "📈 Seasons Evolution",
        "🎯 Position Distribution",
        "🏁 Circuit Performance"
    ])
    
    with tab1:
        st.markdown("### Season Progress")
        fig = plot_driver_stats(season_summary, driver_id)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.markdown("### Final Positions Analysis")
        fig = plot_position_distribution(position_dist, driver_id)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3: 
        st.markdown("### Performance by Circuit")
        fig = plot_circuit_performance(circuit_stats, driver_id)
        st.plotly_chart(fig, use_container_width=True)