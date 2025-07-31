
import streamlit as st

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