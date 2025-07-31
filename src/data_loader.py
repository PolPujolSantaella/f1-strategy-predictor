import pandas as pd
import os
import streamlit as st

DATA_PATH = "data/original"

@st.cache_data
def load_drivers():
    return pd.read_csv(os.path.join(DATA_PATH, "drivers.csv"))

@st.cache_data
def load_races():
    return pd.read_csv(os.path.join(DATA_PATH, "races.csv"))

@st.cache_data
def load_circuits():
    return pd.read_csv(os.path.join(DATA_PATH, "circuits.csv"))

@st.cache_data
def load_results():
    return pd.read_csv(os.path.join(DATA_PATH, "results.csv"))

@st.cache_data
def load_constructors():
    return pd.read_csv(os.path.join(DATA_PATH, "constructors.csv"))

@st.cache_data
def get_driver_stats(driverRef: str):
    """Obtener estadísticas completas de un piloto"""
    drivers = load_drivers()
    races = load_races()
    results = load_results()
    constructors = load_constructors()
    circuits = load_circuits()

    driver_info = drivers[drivers['driverRef'] == driverRef]
    if driver_info.empty:
        return None, None, None, None

    driver_id = driver_info.iloc[0]['driverId']
    driver_results = results[results['driverId'] == driver_id]
    driver_races = driver_results.merge(races, on='raceId')
    driver_races = driver_races.merge(constructors, on='constructorId')
    driver_races = driver_races.merge(circuits, on='circuitId')

    # 1. Evolución por temporada
    season_summary = (
        driver_races.groupby('year')
        .agg({
            'points': 'sum',
            'positionOrder': lambda x: (x == 1).sum(),  # Número de victorias
            'grid': lambda x: (x == 1).sum(),           # Poles
            'raceId': 'count',                          # Carreras totales
        })
        .rename(columns={'positionOrder': 'wins', 'grid': 'poles', 'raceId': 'races'})
        .reset_index()
    )
    
    # Calcular podios (posiciones 1, 2, 3)
    podium_counts = driver_races.groupby('year')['positionOrder'].apply(
        lambda x: ((x >= 1) & (x <= 3)).sum()
    ).reset_index(name='podiums')
    season_summary = season_summary.merge(podium_counts, on='year')
    
    # Calcular DNFs
    dnf_counts = driver_races.groupby('year')['positionOrder'].apply(
        lambda x: (x == 0).sum()
    ).reset_index(name='dnf')
    season_summary = season_summary.merge(dnf_counts, on='year')

    # 2. Distribución de posiciones
    if not driver_races.empty and 'positionOrder' in driver_races.columns:
        pos_counts = driver_races['positionOrder'].dropna().value_counts().sort_index()
        if not pos_counts.empty:
            position_distribution = pos_counts.reset_index()
            position_distribution.columns = ['Position', 'Count']
            position_distribution['Position'] = position_distribution['Position'].apply(
                lambda x: 'DNF' if x == 0 else str(int(x))
            )
        else:
            position_distribution = pd.DataFrame(columns=['Position', 'Count'])
    else:
        position_distribution = pd.DataFrame(columns=['Position', 'Count'])

    # 3. Rendimiento por circuito
    circuit_stats = (
        driver_races.groupby('name')
        .agg({
            'positionOrder': lambda x: (x == 1).sum(),  # wins
            'raceId': 'count',
            'lat': 'first',
            'lng': 'first',
            'location': 'first',
            'country': 'first',
        })
        .rename(columns={'positionOrder': 'wins', 'raceId': 'races'})
        .reset_index()
    )

    return season_summary, position_distribution, circuit_stats, driver_info.iloc[0]
