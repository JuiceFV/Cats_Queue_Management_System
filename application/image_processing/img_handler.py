"""

"""
from PIL import Image
from io import BytesIO
import requests


def get_image_as_byte():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    img_resp = requests.get(response.json()[0]['url'])
    return img_resp.content
