import streamlit as st
import pandas as pd
import requests
from src.data_loader import load_drivers



def get_image_from_wikipedia(url):
    try:
        title = url.split("/wiki/")[-1]
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(api_url)
        data = response.json()
        
        return data.get("thumbnail", {}).get("source")
    except:
        return None

pilot_images = {
    "Hamilton": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Lewis_Hamilton_2022_S%C3%A3o_Paulo_Grand_Prix_%2852498120773%29_%28cropped%29.jpg"
}

