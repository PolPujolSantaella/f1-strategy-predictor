import requests

DEFAULT_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"

def get_image_from_wikipedia(url):
    try:
        if not url or "/wiki/" not in url:
            return DEFAULT_IMG_URL
        
        title = url.split("/wiki/")[-1]
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        image_url = data.get("thumbnail", {}).get("source")

        if image_url and image_url.endswith((".jpg", ".jpeg", ".png", ".webp")):
            return image_url
        else:
            return DEFAULT_IMG_URL

    except requests.RequestException as e:
        print(f"Error fetching image from Wikipedia: {e}")
        return DEFAULT_IMG_URL
