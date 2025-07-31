import streamlit as st 
import pandas as pd
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


st.set_page_config(
    page_title="F1 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏎️"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
        
    from src.data_loader import load_drivers, load_circuits, get_driver_stats
    from src.url_images import pilot_images, get_image_from_wikipedia
    from src.visualizations import (
                                    plot_driver_stats,
                                    plot_position_distribution,
                                    plot_circuit_performance
                                    )
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

def load_css():
    st.markdown("""
    <style>
    /* CSS Variables */
    :root {
        --primary-color: #FF1801;
        --secondary-color: #000000;
        --accent-color: #FFD700;
        --bg-color: #FFFFFF;
        --text-color: #333333;
        --card-bg: #F8F9FA;
    }
    
    /* Principal Style */
    .main {
        padding-top: 2rem;
    }
    
    /* Principal Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    -main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--card-bg);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    
    .sidebar-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Radio buttons styling */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stRadio label {
        font-size: 1.3rem !important;
        font-weight: 600 !important; 
        color: white !important;
    }
    
    /* Card & Containers */
    .stat-card {
        background-color: var(--card-bg);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--primary-color);
        margin: 1rem 0;
    }
    
    .driver_info {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .driver_name {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .driver-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .detail-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 3px solid var(--accent-color);
    }
    
    .detail-label {
        font-weight: 600;
        color: var(--text-color);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .detail-value {
        font-size: 1.1rem;
        color: var(--primary-color);
        font-weight: 500;
        margin-top: 0.3rem;
    }
    
    /* Metrics */
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .metric-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-top: 4px solid var(--primary-color);
        min-width: 150px;
        flex: 1;
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        display: block;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-color);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Buttons  */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), #d4001a);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 24, 1, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 24, 1, 0.4);
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e9ecef;
    
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(255, 24, 1, 0.1);
    }
    
    /* Alerts  */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    
    .stError {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main_header h1 {
            font-size: 2rem;
        }
        .driver_name {
            font-size: 2rem;
        }
        .metric-container {
            flex-direction: column;
        }
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stat-card, .driver_info, .metric-box {
        animation: fadeIn 0.6s ease-in-out;
    }
    
    /* Soft Scroll */
    html {
        scroll-behavior: smooth;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
def create_header():
    """Create the main header for the app."""
    st.markdown("""
    <div class="main-header">
        <h1>🏎️ F1 Dashboard</h1>
        <p>Explore the history of Formula 1 from 1950 to 2024 </p>
        <p>Analyze drivers, teams, circuits and predict results</p>
    </div>
    """, unsafe_allow_html=True)
    
def create_sidebar():
    """Create the sidebar with navigation options."""
    if os.path.exists("img/f1_logo.jpg"):
        st.sidebar.image("img/f1_logo.jpg", width=180)
    
    st.sidebar.markdown('<div class="sidebar-title">📊 Analysis</div>', unsafe_allow_html=True)

    option = st.sidebar.radio("",
        ["📍 Circuits", "🏁 Pilots", "📅 Races"],
        key="navigation"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Caracteristics:**
    - Historical data from 1950 to 2024
    - Analysis of drivers
    - Statistics of circuits
    - Interactive visualizations
    """)
    
    return option
def display_driver_metrics(season_summary, position_dist):
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
                <span class="metric-label">Carreras</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{}</span>
                <span class="metric-label">Victorias</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{}</span>
                <span class="metric-label">Podios</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{:.1f}%</span>
                <span class="metric-label">% Victorias</span>
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
        
        col1, col2 = st.columns([2, 1])
        with col1:
            pilot_selected = st.selectbox(
                "Select a driver for statistics:",
                pilots,
                key="pilot_select"
            )
        
        with col2:
            if st.button("🔄 Refresh Data", key="refresh_pilot"):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if pilot_selected:
            pilot_data = df[df['surname'] == pilot_selected].iloc[0]
            
            # Información del piloto con diseño mejorado
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Imagen del piloto
                wiki_url = pilot_data.get("url", "")
                if wiki_url:
                    img_url = get_image_from_wikipedia(wiki_url)
                    if img_url:
                        st.image(img_url, width=300, caption=f"{pilot_data['forename']} {pilot_data['surname']}")
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
                        <div class="detail-item">
                            <div class="detail-label">Code</div>
                            <div class="detail-value">{pilot_data.get('code', 'N/A')}</div>
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
            display_driver_metrics(season_summary, position_dist)
            
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
                
    except Exception as e:
        st.error(f"❌ Error al cargar los datos de pilotos: {str(e)}")

def display_circuits_section():
    """Sección de circuitos mejorada"""
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### 🏁 Análisis de Circuitos")
    
    try:
        df = load_circuits()
        circuits = sorted(df["name"].dropna().unique())
        
        col1, col2 = st.columns([2, 1])
        with col1:
            circuit_selected = st.selectbox(
                "Selecciona un circuito para ver sus estadísticas:",
                circuits,
                key="circuit_select"
            )
        
        with col2:
            if st.button("🔄 Actualizar", key="refresh_circuit"):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if circuit_selected:
            circuit_data = df[df['name'] == circuit_selected].iloc[0]
            
            # Información del circuito
            st.markdown(f"""
            <div class="driver-info">
                <div class="driver-name">🏁 {circuit_data['name']}</div>
                <div class="driver-details">
                    <div class="detail-item">
                        <div class="detail-label">Ubicación</div>
                        <div class="detail-value">{circuit_data['location']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">País</div>
                        <div class="detail-value">{circuit_data['country']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Latitud</div>
                        <div class="detail-value">{circuit_data.get('lat', 'N/A')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Longitud</div>
                        <div class="detail-value">{circuit_data.get('lng', 'N/A')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Aquí podrías agregar más análisis específicos del circuito
            st.info("💡 Funcionalidad de análisis detallado de circuitos en desarrollo.")
            
    except Exception as e:
        st.error(f"❌ Error al cargar los datos de circuitos: {str(e)}")

def display_races_section():
    """Sección de carreras"""
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### 🏆 Análisis de Carreras")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("🚧 Sección de análisis de carreras en desarrollo.")
    st.markdown("""
    **Próximas funcionalidades:**
    - Análisis de carreras por temporada
    - Estadísticas de equipos
    - Comparación entre temporadas
    - Análisis de pole positions y vueltas rápidas
    """)

def display_statistics_section():
    """Sección de estadísticas generales"""
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Estadísticas Generales")
    st.markdown('</div>', unsafe_allow_html=True)
    
    try:
        df_drivers = load_drivers()
        df_circuits = load_circuits()
        
        # Estadísticas generales
        total_drivers = len(df_drivers)
        total_circuits = len(df_circuits)
        countries_drivers = df_drivers['nationality'].nunique()
        countries_circuits = df_circuits['country'].nunique()
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-box">
                <span class="metric-number">{total_drivers}</span>
                <span class="metric-label">Pilotos Total</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{total_circuits}</span>
                <span class="metric-label">Circuitos</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{countries_drivers}</span>
                <span class="metric-label">Países (Pilotos)</span>
            </div>
            <div class="metric-box">
                <span class="metric-number">{countries_circuits}</span>
                <span class="metric-label">Países (Circuitos)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gráficos adicionales
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Nacionalidades de Pilotos")
            nationality_counts = df_drivers['nationality'].value_counts().head(10)
            fig_nat = px.bar(
                x=nationality_counts.values,
                y=nationality_counts.index,
                orientation='h',
                title="Distribución por Nacionalidad",
                color=nationality_counts.values,
                color_continuous_scale='Reds'
            )
            fig_nat.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            st.plotly_chart(fig_nat, use_container_width=True)
        
        with col2:
            st.markdown("#### Circuitos por País")
            country_counts = df_circuits['country'].value_counts().head(10)
            fig_countries = px.pie(
                values=country_counts.values,
                names=country_counts.index,
                title="Distribución de Circuitos"
            )
            st.plotly_chart(fig_countries, use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ Error al cargar estadísticas generales: {str(e)}")

def main():
    """Función principal"""
    # Cargar CSS personalizado
    load_css()
    
    # Header principal
    create_header()
    
    # Sidebar con navegación
    option = create_sidebar()
    
    # Contenido principal basado en la selección
    if option == "🏁 Pilots":
        display_pilots_section()
    elif option == "📍 Circuits":
        display_circuits_section()
    elif option == "📅 Races":
        display_races_section()
    elif option == "📈 Estadísticas":
        display_statistics_section()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; opacity: 0.7; margin: 2rem 0;">
        <p>🏎️ F1 Dashboard | Datos históricos 1950-2020 | Hecho con ❤️ y Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()