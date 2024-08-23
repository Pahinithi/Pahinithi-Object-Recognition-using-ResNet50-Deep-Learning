from flask import Flask, request, render_template
import numpy as np
import cv2
from tensorflow import keras
from PIL import Image

# Create a Flask application instance
app = Flask(__name__)

# Load the trained model
model = keras.models.load_model('Objmodel.h5')

# Define a route for the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Define a route for making predictions
@app.route("/predict", methods=["POST"])
def predict():
    # Get the uploaded file
    file = request.files['image']
    if file:
        # Process the uploaded image
        img = Image.open(file)
        img = img.resize((32, 32))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Make a prediction using the model
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)[0]
        
        # Mapping predicted class to label
        labels_dictionary = {0: 'airplane', 1: 'automobile', 2: 'bird', 3: 'cat', 
                             4: 'deer', 5: 'dog', 6: 'frog', 7: 'horse', 
                             8: 'ship', 9: 'truck'}
        prediction_text = f'The predicted class for the image is: <strong>{labels_dictionary[predicted_class]}</strong>'
        
        return render_template("index.html", prediction=prediction_text)
    return render_template("index.html", prediction="No image uploaded.")

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
