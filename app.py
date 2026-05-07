from flask import Flask, request
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

app = Flask(__name__)

# Load trained model
model = load_model("tooth_decay_model.keras")

@app.route("/")
def home():
    return "Tooth Decay Detection API Running"

@app.route("/predict", methods=["POST"])
def predict():

    # get uploaded file
    file = request.files["file"]

    # convert file to image
    img = Image.open(io.BytesIO(file.read()))

    # resize image
    img = img.resize((224, 224))

    # convert to array
    img_array = image.img_to_array(img) / 255.0

    # expand dimensions
    img_array = np.expand_dims(img_array, axis=0)

    # prediction
    prediction = model.predict(img_array)[0][0]

    if prediction > 0.5:
        result = "Tooth Decay Detected"
    else:
        result = "No Tooth Decay"

    return result


if __name__ == "__main__":
    app.run(debug=True)