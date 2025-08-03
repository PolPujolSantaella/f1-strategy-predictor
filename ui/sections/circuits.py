
import streamlit as st
from src.data_loader import load_circuits, get_winners_circuits, get_constructor_winners
from src.url_images import get_image_from_wikipedia
from src.visualizations import display_top3_winners_cards, display_top3_constructors_cards
from typing import Optional


def display_circuits_section() -> None:
    """
    Display the circuits analysis section.
    Allows selecting a circuit to view its details, image, and top winners.
    """
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown("### 🏁 Circuit Analysis")
    
    try:
        df = load_circuits()
        circuits = sorted(df["name"].dropna().unique())
        
        selected_circuit  = st.selectbox(
            "Select a circuit to view its statistics:",
            circuits,
            key="circuit_select"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_circuit :
            circuit_data = get_circuit_data(df, selected_circuit)
            display_circuit_info(circuit_data)
            
            wiki_url = circuit_data.get("url", "")
            display_circuit_image(wiki_url, circuit_data.get('name', ''))
            
            st.markdown("### Circuit Analysis")
            
            tab1, tab2, = st.tabs(["🏆 TOP 3 Winners", "🏆 TOP 3 Constructor Winners"])
            
            with tab1:
                winners = get_winners_circuits(selected_circuit)
                display_top3_winners_cards(winners)
                
            with tab2:
                constructor_winners = get_constructor_winners(selected_circuit)
                display_top3_constructors_cards(constructor_winners)
                
    except (KeyError, IndexError, ValueError) as e:
        st.error(f"Error processing circuit data: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error loading circuits data.")
        raise e
    

def get_circuit_data(df, circuit_name: str) -> dict:
    """Fetch data for the selected circuit from DataFrame."""
    circuit_row = df[df['name'] == circuit_name]
    if circuit_row.empty:
        raise ValueError(f"Circuit '{circuit_name}' not found.")
    return circuit_row.iloc[0].to_dict()


def display_circuit_info(circuit_data: dict) -> None:
    """Render the circuit's details in styled HTML."""
    st.markdown(
        f"""
        <div class="driver-info">
            <div class="driver-name">🏁 {circuit_data.get('name', 'N/A')}</div>
            <div class="driver-details">
                <div class="detail-item"><div class="detail-label">Location</div><div class="detail-value">{circuit_data.get('location', 'N/A')}</div></div>
                <div class="detail-item"><div class="detail-label">Country</div><div class="detail-value">{circuit_data.get('country', 'N/A')}</div></div>
                <div class="detail-item"><div class="detail-label">Latitude</div><div class="detail-value">{circuit_data.get('lat', 'N/A')}</div></div>
                <div class="detail-item"><div class="detail-label">Longitude</div><div class="detail-value">{circuit_data.get('lng', 'N/A')}</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
def display_circuit_image(wiki_url: Optional[str], circuit_name: str) -> None:
    """Fetch and display circuit image from Wikipedia or show fallback messages."""
    if wiki_url:
        image_url = get_image_from_wikipedia(wiki_url)
        if image_url:
            st.image(image_url, caption=f"View of {circuit_name}", use_container_width=True)
        else:
            st.warning("Circuit image not available.")
    else:
        st.info("Wikipedia URL not available for this circuit.")