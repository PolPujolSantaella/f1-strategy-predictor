
import streamlit as st
from src.data_loader import load_circuits
from src.url_images import get_image_from_wikipedia


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
            
            wiki_url = circuit_data.get("url", "")
            if wiki_url:
                image_url = get_image_from_wikipedia(wiki_url)
                if image_url:
                    st.image(image_url, caption=f"Vista de {circuit_data['name']}", use_container_width=True)
                else:
                    st.warning("📷 Imagen del circuito no disponible.")
            else:
                st.info("🌐 URL de Wikipedia no disponible para este circuito.")
                        
                st.markdown("#### Análisis de Circuito")    
                
                          
            # Aquí podrías agregar más análisis específicos del circuito
            st.info("💡 Funcionalidad de análisis detallado de circuitos en desarrollo.")
            
    except (KeyError, IndexError, ValueError) as e:
        st.error(f"❌ Error al procesar los datos de circuitos: {str(e)}")
    except Exception as e:
        st.error("❌ Ocurrió un error inesperado al cargar los circuitos.")
        raise e  
