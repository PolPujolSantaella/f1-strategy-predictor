import streamlit as st
from menu_options import MENU_OPTIONS
from src.styles import load_css
from ui.header import create_header
from ui.sidebar import create_sidebar
from ui.sections import drivers, circuits, races, comparison

def main() -> None:
    """Run the main F1 dashboard app."""
    
    load_css()
    create_header()
    
    selected_option = create_sidebar()
    display_section(selected_option)
    
    footer()



def display_section(option: str) -> None:
    """Render the appropriate section based on sidebar option. """
    
    if option == MENU_OPTIONS["PILOTS"]:
        drivers.display_driver_section()
    elif option == MENU_OPTIONS["CIRCUITS"]:
        circuits.display_circuits_section()
    elif option == MENU_OPTIONS["RACES"]:
        races.display_races_section()
    elif option == MENU_OPTIONS["COMPARE"]:
        comparison.display_comparison_section()
    else:
        st.warning("Select an option from the sidebar.")


def footer() -> None:
    """Display footer information."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; opacity: 0.7;">
            🏎️ F1 Dashboard | POL PUJOL SANTAELLA
        </div>
        """,
        unsafe_allow_html=True,
    )
    
if __name__ == "__main__":
    main()