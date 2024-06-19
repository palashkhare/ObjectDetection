import os
import logging

from ultralytics import YOLO
from PIL import Image


BASE_PATH = os.environ.get("HOME")
logger = logging.getLogger("Prediction")
logging.basicConfig(format="%(asctime)s %(levelname)s : %(message)s", level=logging.DEBUG)


class YoloObjectDetection:

    def __init__(self, model_size="yolov8m.pt"):
        self.model_size = model_size
        self.model: YOLO = self._init_model()
        self.prediction_results = None

    def _init_model(
        self,
    ):
        return YOLO(self.model_size)

    def get_info(
        self,
    ):
        if self.prediction_results:
            return {
                "Number of boxes": len(self.result.boxes),
            }
        logging.info("Provide an image to predict")

    def predict(self, image, return_image=False, **kwargs):
        self.prediction_results = None  # Clean buffer
        self.prediction_results = self.model.predict(image, **kwargs)
        result = self.prediction_results[0]
        if return_image:
            return (
                self._get_annotation_box_coordinates(result.boxes),
                result.plot()[:, :, ::-1],
            )
        return (self._get_annotation_box_coordinates(result.boxes),)

    def _get_annotation_box_coordinates(self, boxes):
        annotations = []
        for box in boxes:
            annotations.append(
                {
                    "object_id": box.cls[0].item(),
                    "object_name": self.get_annotation_dict().get(box.cls[0].item()),
                    "coordinates": box.xyxy[0].tolist(),
                    "probability": round(box.conf[0].item(), 2),
                }
            )
        return {"boxes": len(boxes), "annotations": annotations}

    def get_annotation_dict(self, ):
        if self.prediction_results:
            return self.prediction_results[0].names

# m = YoloObjectDetection()
# result, img = m.predict("datasets/mumbai-led-light-traffic-signal-2021-600x338.jpg", return_image=True)
# im = Image.fromarray(img)
# im.save("test.jpeg")
# print(result)