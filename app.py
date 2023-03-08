# import
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras_preprocessing import image
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import uuid
import os

# Server name
name = "Covid Server"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# model load & class_type
model = keras.models.load_model("model/CXR.h5")
class_type = {0: 'Covid', 1: 'Normal'}

# Limit image size to prevent denial of service attacks
MAX_IMAGE_SIZE = 16 * 1024 * 1024

# limit the file extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# processing
def pre_process_image(img_path):
    path = img_path
    img = image.load_img(path, target_size=(224, 224, 3))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img


app = Flask(__name__)
CORS(app)


@app.route("/map/12va@", methods=["GET"])
def map():
    if request.method == "GET":
        return jsonify({"api_map": "Ap4sdbO1kaU7yqyU9dKUBrZ3weX3kGKfO6M0Fp_dYMvx0ksXZnr-pcxs5W8-usYv"})


@app.route("/rapid_host/12vs@", methods=["GET"])
def rapid_host():
    if request.method == "GET":
        return jsonify({"rapid_host": "covid-193.p.rapidapi.com"})


@app.route("/rapid_api/12api@", methods=["GET"])
def rapid_api():
    if request.method == "GET":
        return jsonify({"rapid_api": "9bd84acd11mshac5226ef20ab044p121ad6jsn1cd5cc86bf7c"})


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #file
        file = request.files.get('file')
        
        # check 1
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            # check 2
            if (file and '.' in file.filename):
                path = file.filename.rsplit(".")
                extension = path.pop()
            if (extension not in ALLOWED_EXTENSIONS):
                return jsonify({"error": extension+": Invalid Extension"})

            # Delete the file contents
            dir = 'upload/'
            if os.listdir(dir) != 0:
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))

            # Use the uuid4 to store
            filename = str(uuid.uuid4()) + ".png"
            file.save("upload/" + filename)

            try:
                imgf = Image.open("upload/"+filename)
                if not is_lung_xray_image(imgf):
                    return jsonify({"error": "Invalid X-Ray Image. Please upload a valid lung x-ray image."})

            except Exception as e:
                print(e)

            img = pre_process_image("upload/"+filename)
            covid = model.predict(img)[0][0]*100
            normal = model.predict(img)[0][1]*100

            print("covid", covid)
            print("normal", normal)

            if (covid > normal):
                prediction = "Covid"
            else:
                prediction = "Normal"

            data = prediction
            return jsonify({"result": data})

        except Exception as e:
            return jsonify({"error": str(e)})

    return jsonify(name)


def is_lung_xray_image(img):

    # check if the image is in grayscale format
    # need to check

    width, height = img.size
    if(width*height > MAX_IMAGE_SIZE):
        return False

    aspect_ratio = width / height
    if not (0.7 <= aspect_ratio <= 1.5):
        return False
    
    return True


if __name__ == "__main__":
    app.run()