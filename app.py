import os
from flask import Flask, render_template, request
from deep_learning_model import YoloOCR  # Assuming your class is named YoloOCR

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static/upload/')
CROPPED_PATH = './static/predict/crops/number-plate/'

# Initialize the YoloOCR instance
yolo_ocr = YoloOCR()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        save_path = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(save_path)
        cropped_image_name = os.path.join(CROPPED_PATH, filename)
        print('Cropped image', cropped_image_name)

        try:
            # Perform YOLO detection and OCR
            results = yolo_ocr.perform_yolo_detection(image_path=save_path)
            cropped_image=yolo_ocr.show_image(cropped_image_name)
            extracted_text = yolo_ocr.ocr_image(cropped_image)
        except Exception as e:
            return render_template('error.html', error_message=str(e))

        return render_template('index.html', upload=True, uploaded_image=filename, text=extracted_text, croped_image=filename)

    return render_template('index.html', upload=False)

if __name__ == '__main__':
    app.run(debug=True)
