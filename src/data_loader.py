import os
import pandas as pd
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
def get_driver_stats(driver_ref: str):
    """Return statistics of a specific driver."""
    drivers = load_drivers()
    races = load_races()
    results = load_results()
    constructors = load_constructors()
    circuits = load_circuits()

    driver_info = drivers[drivers['driverRef'] == driver_ref]
    if driver_info.empty:
        return None, None, None, None

    driver_id = driver_info.iloc[0]['driverId']
    driver_results = results[results['driverId'] == driver_id]
    driver_races = (
        driver_results
        .merge(races, on='raceId')
        .merge(constructors, on='constructorId')
        .merge(circuits, on='circuitId')
    )
    
    # 1. Season Summary
    season_summary = (
        driver_races.groupby('year')
        .agg({
            'points': 'sum',
            'positionOrder': lambda x: (x == 1).sum(),  # wins
            'grid': lambda x: (x == 1).sum(),           # poles
            'raceId': 'count',                          # races
        })
        .rename(columns={'positionOrder': 'wins', 'grid': 'poles', 'raceId': 'races'})
        .reset_index()
    )
    
    podiums = driver_races.groupby('year')['positionOrder'].apply(
        lambda x: ((x >= 1) & (x <= 3)).sum()
    ).reset_index(name='podiums')
    
    dnfs = driver_races.groupby('year')['positionOrder'].apply(
        lambda x: (x == 0).sum()
    ).reset_index(name='dnf')
    
    season_summary = (
        season_summary
        .merge(podiums, on='year')
        .merge(dnfs, on='year')
    )

    # 2. Position Distribution
    position_distribution = (
        driver_races['positionOrder']
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )
    
    position_distribution.columns = ['Position', 'Count']
    position_distribution['Position'] = position_distribution['Position'].apply(
        lambda x: 'DNF' if x == 0 else str(int(x))
    )
    
    # 3. Performance by Circuit
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


@st.cache_data
def get_winners_circuits(circuit_name: str):
    
    circuits = load_circuits()
    races = load_races()
    results = load_results()
    drivers = load_drivers()
    
    circuit_row = circuits[circuits['name'] == circuit_name]
    merged_df = races.merge(circuit_row, on="circuitId")
    merged_df = merged_df.merge(results, on="raceId")
    merged_df = merged_df.merge(drivers, on="driverId")
    
    winners_df = merged_df[merged_df['positionOrder'] == 1]
  
    top_winners = (
        winners_df
        .groupby(["url", "forename", "surname"])["positionOrder"]
        .count()
        .reset_index()
        .rename(columns={"positionOrder": "wins"})
        .sort_values(by="wins", ascending=False)
        .head(3)
    )
    
    top_winners["driver"] = top_winners["surname"]
    
    return top_winners

@st.cache_data
def get_constructor_winners(circuit_name: str):
    circuits = load_circuits()
    races = load_races()
    results = load_results()
    constructors = load_constructors()
    
    circuit_row = circuits[circuits['name'] == circuit_name]
    merged_df = races.merge(circuit_row, on="circuitId")
    merged_df = merged_df.merge(results, on="raceId")
    merged_df = merged_df.merge(constructors, on="constructorId")
    
    winners_df = merged_df[merged_df['positionOrder'] == 1]
  
    top_constructors = (
        winners_df
        .groupby(["url", "name"])["positionOrder"]
        .count()
        .reset_index()
        .rename(columns={"positionOrder": "wins"})
        .sort_values(by="wins", ascending=False)
        .head(3)
    ) 
    
    top_constructors["constructor"] = top_constructors["name"]
    
    return top_constructors