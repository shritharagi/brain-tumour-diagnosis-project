from flask import Flask, request, render_template
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simulate ML model loading
def predict_tumor(img_path):
    # In real scenario, load your trained model and predict
    # Here we simulate prediction based on image size
    try:
        img = Image.open(img_path).convert('RGB').resize((128, 128))
        img_array = np.array(img) / 255.0
        # Simulate prediction
        prediction = np.random.rand()  # fake prediction score between 0 and 1
        return "Tumor Detected" if prediction > 0.5 else "No Tumor"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result = predict_tumor(filepath)
            return render_template('result.html', result=result, image_file=filename)
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)