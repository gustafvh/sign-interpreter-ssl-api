import requests

API_URL = "http://localhost:5000/predict"
IMAGE_PATH = "H2.jpg"

# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()
payload = {"image": image}

# submit the request
response = requests.post(API_URL, files=payload).json()
print(response)
