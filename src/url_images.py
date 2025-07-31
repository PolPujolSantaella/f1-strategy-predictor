import requests

def get_image_from_wikipedia(url):
    try:
        title = url.split("/wiki/")[-1]
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return data.get("thumbnail", {}).get("source")
    except requests.RequestException as e:
        print(f"Error fetching image from Wikipedia: {e}")
        return None



