import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import streamlit as st

def plot_driver_stats(df: pd.DataFrame, driver_name: str):
    """
    Plot statistics for a specific F1 driver.
    
    Parameters:
    - df: DataFrame containing F1 data.
    - driver_name: Name of the driver to plot statistics for.
    """
    
    driver_df = df[df['driver'] == driver_name]
    
    if driver_df.empty:
        st.warning("No data available for the selected driver.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(data=driver_df, x='year', y='positionOrder', marker='o', ax=ax)
    
    ax.invert_yaxis()
    ax.set_title(f"Positions of {driver_name} for championship")
    ax.set_xlabel("Year")
    ax.set_ylabel("Final Position")
    
    st.pyplot(fig)