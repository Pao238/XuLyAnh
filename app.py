from flask import Flask, render_template, request
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

# dùng opencv,numpy biến đổi
def apply_transformation(image, transformation_type):
    if transformation_type == 'negative':
        # âm bản
        # 255-px
        return 255 - image
    elif transformation_type == 'threshold':
        # binary
        _, thresholded_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        return thresholded_image
    elif transformation_type == 'gray':     
        # xám
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            return image
    elif transformation_type == 'logarithm':
        return np.uint8(255 / np.log(1 + np.max(image)) * (np.log(np.float32(image) + 1)))
    elif transformation_type == 'power':
        # biến đổi tuyến tính theo hàm mũ
        return np.power(image, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_image_path = None
    transformed_image_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            print(file.filename)
            image_bytes = BytesIO(file.read())
            image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            transformation_type = request.form.get('transformation_type')
            
            transformed_image = apply_transformation(image, transformation_type)

            # Đường dẫn ảnh
            original_image_path = "static/"+file.filename
            transformed_image_path = "static/after pic.jpg"
            
            cv2.imwrite(transformed_image_path, transformed_image)

    return render_template('index.html', original_image_path=original_image_path, transformed_image_path=transformed_image_path)

if __name__ == '__main__':
    app.run(debug=True)
