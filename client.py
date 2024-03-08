import requests
import os

from PIL import Image
# URL for the Flask application
base_url = 'http://127.0.0.1:5000/api/'

# Read ID card
image_path = 'temp.jpg'
files = {'image': open(image_path, 'rb')}
response = requests.post(base_url + 'read_id_card', files=files)
print(response.json())

# Fill out form
form_data = {
    # Form data here (e.g., name, address, etc.)
}
response = requests.post(base_url + 'fill_form', json=form_data)
print(response.json())
