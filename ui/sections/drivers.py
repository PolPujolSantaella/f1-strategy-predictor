import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_drivers, get_driver_stats
from src.url_images import get_image_from_wikipedia
from src.visualizations import (
    plot_driver_stats,
    plot_position_distribution,
    plot_circuit_performance
)


def display_driver_metrics(season_summary):
    """Mostrar métricas clave del piloto"""
    if season_summary is not None and not season_summary.empty:
        total_races = season_summary['races'].sum()
        total_wins = season_summary['wins'].sum()
        total_podiums = season_summary['podiums'].sum()
        win_rate = (total_wins / total_races * 100) if total_races > 0 else 0
        
        st.markdown("""
        <div class="metric-container">
            <div class="metric-box">
                <span class="metric-number">{}</span>
                <span class="metric-label">Races</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{}</span>
                <span class="metric-label">Victories</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{}</span>
                <span class="metric-label">Podiums</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{:.1f}%</span>
                <span class="metric-label">% Victories</span>
            </div>
        </div>
        """.format(total_races, total_wins, total_podiums, win_rate), unsafe_allow_html=True)
        
        

def display_pilots_section():
    """Sección de pilotos mejorada"""
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Select Driver")
    
    try:
        df = load_drivers()
        pilots = sorted(df["surname"].dropna().unique())
        
        pilot_selected = st.selectbox(
            "Select a driver for statistics:",
            pilots,
            key="pilot_select"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if pilot_selected:
            pilot_data = df[df['surname'] == pilot_selected].iloc[0]
            
            # Información del piloto con diseño mejorado
            col1, col2 = st.columns(2)
            
            with col1:
                # Imagen del piloto
                wiki_url = pilot_data.get("url", "")
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
                        st.info("Image not available")
                else:
                    st.info("Image not available")
            
            with col2:
                # Información detallada
                st.markdown(f"""
                <div class="driver-info">
                    <div class="driver-name">{pilot_data['forename']} {pilot_data['surname']}</div>
                    <div class="driver-details">
                        <div class="detail-item">
                            <div class="detail-label">Number</div>
                            <div class="detail-value">{pilot_data['number'] if pd.notna(pilot_data['number']) else 'N/A'}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Date of Birth</div>
                            <div class="detail-value">{pilot_data['dob']}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Nationality</div>
                            <div class="detail-value">{pilot_data['nationality']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Obtener estadísticas
            with st.spinner(f"Cargando estadísticas de {pilot_selected}..."):
                season_summary, position_dist, circuit_stats, _ = get_driver_stats(pilot_selected)
            
            if season_summary is None or season_summary.empty:
                st.warning("No data available for this driver.")
                return
            
            # Métricas principales
            display_driver_metrics(season_summary)
            
            # Gráficos en tabs
            tab1, tab2, tab3 = st.tabs(["📈 Seasons Evolution", "🎯 Positions Distributions", "🏁 Performance for Circuit"])
            
            with tab1:
                st.markdown("#### Season progress")
                fig_season = plot_driver_stats(season_summary, pilot_selected)
                st.plotly_chart(fig_season, use_container_width=True)
            
            with tab2:
                st.markdown("#### Final Positions Analysis")
                fig_position = plot_position_distribution(position_dist, pilot_selected)
                st.plotly_chart(fig_position, use_container_width=True)
            
            with tab3:
                st.markdown("#### Performance in diferents circuits")
                fig_circuit = plot_circuit_performance(circuit_stats, pilot_selected)
                st.plotly_chart(fig_circuit, use_container_width=True)
                
    except (KeyError, ValueError, IndexError) as e:
        st.error(f"❌ Error al cargar los datos de pilotos: {str(e)}")
