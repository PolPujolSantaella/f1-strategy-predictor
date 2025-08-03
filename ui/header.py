import streamlit as st

def create_header() -> None:
    """Render the main header for the F1 Dashboard app."""
    st.markdown(
        """
        <div class="main-header">
            <h1>🏎️ F1 Dashboard</h1>
            <p>Explore the history of Formula 1 from 1950 to 2024 </p>
            <p>Analyze drivers, teams, circuits and predict results</p>
        </div>
        """, 
        unsafe_allow_html=True
    )