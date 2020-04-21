from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet import preprocess_input

from tensorflow.keras import models
from PIL import Image
import numpy as np
import flask
import io

# Boot up production server with:
# gunicorn -b 127.0.0.1:5000 main:app

# Boot up development server with:
# py main.py

# Make request with curl (or programmatically with testRequest.py:
# curl -X POST -F image=@H2.jpg 'http://localhost:5000/predict'
# curl -X POST -F image=@H2.jpg 'http://35.198.151.110/predict'
# Gives Response:
# {"letterSent":"H","predictions":[["H",100.0],["C",0.0],["F",0.0]]}

app = flask.Flask(__name__)
model = None

def load_model():
    global model
    model = models.load_model("./assets/model-quiet-dew-32.h5")


def prepare_image(image, target):

    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    return image


@app.route("/", methods=["POST"])

def index():
    return flask.jsonify("Connected to API.")

@app.route("/predict", methods=["POST"])

def predict():
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            image = prepare_image(image, target=(224, 224))

            predictions = model.predict(image)

            predictions = getTopPredictions(predictions[0])
            predictions = serialisePreds(predictions)
            response = {
                'success': True,
                'predictions': [{
                    'letter': predictions[0][0],
                    'confidence': predictions[0][1]},{
                    'letter': predictions[1][0],
                    'confidence': predictions[1][1]},{
                    'letter': predictions[2][0],
                    'confidence': predictions[2][1]
                    }]
            }

    return flask.jsonify(response)

def getTopPredictions(preds):
    predsDict = {
        'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0,
        'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0,
        'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
        'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0, 'A1': 0,
        'A2': 0, 'O1': 0,
    }
    # map preds index with probability to correct letter from dictonary
    for i, key in enumerate(predsDict, start=0):
        predsDict[key] = preds[i]

    # sort by dictonary value and returns as list
    all_preds = sorted(predsDict.items(), reverse=True, key=lambda x: x[1])
    top_preds = [all_preds[0], all_preds[1], all_preds[2]]
    return top_preds, all_preds

def serialisePreds(predictions):
    topPreds = []
    for i, pred in enumerate(predictions[0], start=0):
        letter, confidence = predictions[0][i]
        topPreds.append((letter, round(confidence*100, 8)))
    return topPreds

@app.errorhandler(500)
def internal_server_error(error):
    response = {'success': False}
    return flask.jsonify(response)

print("Loading Model...")
load_model() #Load model before apps run to prevent long loading time
print("Model Loaded. Server Running.")

if __name__ == "__main__":  #if running on development
    app.run(debug=True, threaded=False, host='0.0.0.0')

