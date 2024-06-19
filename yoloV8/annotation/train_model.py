import os
from pathlib import Path

from ultralytics import YOLO


BASE = Path(os.environ.get("HOME"))
model_name = "yolov8m.pt"
model = YOLO(model=model_name)

model.train(data=f"{BASE}/workspace/ObjectDetection/yoloV8/datasets/road_sign_data/data.yaml", epochs=10,)
