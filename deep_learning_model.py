from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from IPython.display import display

# Initialize YOLO model
Yolomodel = YOLO('./static/models/bestn.pt')

# Initialize TrOCR processor and model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")


class YoloOCR:
    def __init__(self, project="./static/", name="", exist_ok=True):
        self.project = project
        self.name = name
        self.exist_ok = exist_ok

    def perform_yolo_detection(self, image_path, save=True, save_crop=True):
        try:
            results = Yolomodel(image_path, save=save, save_crop=save_crop,
                                project=self.project, name=self.name, exist_ok=self.exist_ok)
            return results
        except Exception as e:
            raise Exception(f"Yolo detection failed: {str(e)}")

    def show_image(self, croped_image_name):
        try:
            image_path = croped_image_name
            img = Image.open(image_path).convert("RGB")
            display(img)
            return img
        except Exception as e:
            raise Exception(f"Image display failed: {str(e)}")

    def ocr_image(self, croped_image_name):
        try:
            pixel_values = processor(
                images=croped_image_name, return_tensors="pt").pixel_values
            generated_ids = model.generate(pixel_values)
            extracted_text = processor.batch_decode(
                generated_ids, skip_special_tokens=True)[0]
            return extracted_text
        except Exception as e:
            raise Exception(f"OCR failed: {str(e)}")
