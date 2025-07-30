import pandas as pd
import os

DATA_PATH = "data/original"

def load_data():
    """
    Load the F1 historical data from CSV files in the specified directory.
    """
    
    try:
        results = pd.read_csv(os.path.join(DATA_PATH, "results.csv"))
        drivers = pd.read_csv(os.path.join(DATA_PATH, "drivers.csv"))
        races = pd.read_csv(os.path.join(DATA_PATH, "races.csv"))
        constructors = pd.read_csv(os.path.join(DATA_PATH, "constructors.csv"))
        
        df = results.merge(drivers, on='driverId', how='left') \
            .merge(races, on='raceId', how='left') \
            .merge(constructors, on='constructorId', how='left')

        df['driver'] = df['forename'] + ' ' + df['surname']
        
        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()