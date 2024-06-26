import time
import cv2
import numpy as np
from yoloV8.annotation.predict import YoloObjectDetection
from kafka.worker_consumer import consume, start_parallel_consume
# from kafka.client_consumer

model = YoloObjectDetection()

start_parallel_consume(model=model, processes=5)

## Left here