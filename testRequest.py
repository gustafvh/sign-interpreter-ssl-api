import requests

#API_URL = 'https://sign-interpreter.com/predict'
#API_URL = 'http://35.198.151.110/predict'
API_URL = 'http://localhost:5000/predict'
IMAGE_PATH = "./assets/H2.jpg"

# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()
#print(image)
payload = {"image": image}

# submit the request
response = requests.post(API_URL, files=payload).json()
print(response)
#print(response.get('predictions')[0].get('letter'))


