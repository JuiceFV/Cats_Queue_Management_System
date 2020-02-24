"""

"""
from PIL import Image
from io import BytesIO
import requests


def get_image_url():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    return response.json()[0]['url']
