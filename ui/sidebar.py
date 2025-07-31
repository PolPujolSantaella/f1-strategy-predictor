import os
import streamlit as st

def create_sidebar():
    """Create the sidebar with navigation options."""
    if os.path.exists("img/f1_logo.jpg"):
        st.sidebar.image("img/f1_logo.jpg", width=180)
    
    st.sidebar.markdown('<div class="sidebar-title"> Analysis</div>', unsafe_allow_html=True)

    option = st.sidebar.radio("",
        ["📍 Circuits", "🏁 Pilots", "📅 Races", "🆚 Compare"],
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