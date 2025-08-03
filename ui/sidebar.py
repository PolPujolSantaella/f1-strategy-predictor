import os
import streamlit as st

def create_sidebar():
    """Create the sidebar with navigation options."""
    if os.path.exists("img/f1_logo.jpg"):
        st.sidebar.image("img/f1_logo.jpg", width=180)
    
    st.sidebar.markdown('<div class="sidebar-title"> Analysis</div>', unsafe_allow_html=True)

    option = st.sidebar.radio("Navigation",
        ["📍 Circuits", "🏁 Pilots", "📅 Races", "🆚 Compare"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='margin-top: 150px;'>
        <strong>Characteristics:</strong>
        <ul>
            <li>Historical data from 1950 to 2024</li>
            <li>Analysis of drivers</li>
            <li>Statistics of circuits</li>
            <li>Interactive visualizations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    return option