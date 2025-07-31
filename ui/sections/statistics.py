
import streamlit as st
from src.data_loader import load_drivers, load_circuits
import plotly.express as px


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
            
    except (KeyError, ValueError, IndexError) as e:
        st.error(f"❌ Error al cargar las estadísticas: {str(e)}")
