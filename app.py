import streamlit as st
from src.styles import load_css

from ui.header import create_header
from ui.sidebar import create_sidebar
from ui.sections import drivers, circuits, races

def main():
    load_css()
    create_header()
    option = create_sidebar()
    
    if option == "🏁 Pilots":
        drivers.display_pilots_section()
    
    elif option == "📍 Circuits":
        circuits.display_circuits_section()
    elif option == "📅 Races":
        races.display_races_section()
    
    st.markdown("---")
    st.markdown("""
                <div style="text-align: center; opacity: 0.7;">🏎️ F1 Dashboard | POL PUJOL SANTAELLA </div>""", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()