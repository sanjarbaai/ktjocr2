from io import BytesIO
import requests
from PIL import Image


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    return img