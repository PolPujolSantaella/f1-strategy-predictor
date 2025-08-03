import requests

DEFAULT_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"

def get_image_from_wikipedia(wikipedia_url: str) -> str:
    """
    Fetch the thumbnail image URL from a Wikipedia article.
    
    Parameters:
        wikipedia_url (str): The full Wikipedia URL of the subject.
        
    Returns:
        str: URL to the thumbnail image, or a default placeholder if unavailable.
    """
    
    try:
        if not wikipedia_url or "/wiki/" not in wikipedia_url:
            return DEFAULT_IMG_URL
        
        title = wikipedia_url.split("/wiki/")[-1]
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        image_url = data.get("thumbnail", {}).get("source", "")

        if image_url and image_url.endswith((".jpg", ".jpeg", ".png", ".webp")):
            return image_url

    except requests.RequestException as e:
        print(f"[Wikipedia API Error] Failed to fetch image for '{wikipedia_url}': {e}")
        
    return DEFAULT_IMG_URL
