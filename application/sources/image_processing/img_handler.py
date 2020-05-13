"""In this module places the function which retrieving an image' url from here https://api.thecatapi.com
"""
import requests


def get_image_url():
    """Getting an image' url. using the request-package.
    """
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')
    except requests.RequestException:
        print("Exception occurred while getting an Image!")
    return response.json()[0]['url']
