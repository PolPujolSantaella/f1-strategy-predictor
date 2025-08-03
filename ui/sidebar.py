import os
import streamlit as st
from typing import Literal

MENU_OPTIONS = ["📍 Circuits", "🏁 Pilots", "📅 Races", "🆚 Compare"]

def create_sidebar() -> Literal["📍 Circuits", "🏁 Pilots", "📅 Races", "🆚 Compare"]:
    """
    Create the sidebar with logo, navigation radio, and analysis info.
    
    Returns:
        The selected navigation option as a string literal.
    """
    
    logo_path = "img/f1_logo.jpg"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=180)
        
    st.sidebar.markdown('<div class="sidebar-title">Analysis</div>', unsafe_allow_html=True)

    option = st.sidebar.radio(
        label="Navigation",
        options=MENU_OPTIONS,
        label_visibility="collapsed"
    )
    
    sidebar_footer()
    
    return option


def sidebar_footer() -> None:
    """Display sidebar footer with app characteristics."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='margin-top: 150px;'>
            <strong>Characteristics:</strong>
            <ul>
                <li>Historical data from 1950 to 2024</li>
                <li>Analysis of drivers</li>
                <li>Statistics of circuits</li>
                <li>Interactive visualizations</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )