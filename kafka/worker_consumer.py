import io, os
import typing
import cv2
import atexit
from confluent_kafka import Consumer, Producer
from avro import schema
from avro.io import BinaryDecoder, DatumReader, BinaryEncoder, DatumWriter
import numpy as np
from multiprocessing import Pool
import logging

logging.basicConfig()
logger = logging.getLogger("Worker Consumer")


if typing:
    from yoloV8.annotation.predict import YoloObjectDetection


def consume(model: YoloObjectDetection):
    logger.info(f"{os.getpid()}")
    p = Producer({"bootstrap.servers": "localhost:9092"})
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })
    schema_path = "kafka/schema/frames.avsc"

    with open(schema_path, "r") as f:
        avro_schema = schema.parse(f.read())


    reader = DatumReader(avro_schema)
    writer = DatumWriter(avro_schema)

    c.subscribe(['tpc_x'])

    while True:

        logger.info(f"{os.getpid()}")
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        raw_bytes = msg.value()
        bytes_reader = io.BytesIO(raw_bytes)
        decoder = BinaryDecoder(bytes_reader)
        avro_data = reader.read(decoder=decoder)
        frame = np.frombuffer(avro_data["frame_3d"], dtype=np.uint8).reshape(480, 640, 3)
        prediction, frame = model.predict(frame, return_image=True)
        bytes_reader.flush()
        bytes_reader.close()

        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        avro_data["frame_3d"] = frame.flatten().tobytes()
        writer.write(avro_data, encoder=encoder)
        raw_bytes = bytes_writer.getvalue()
        p.produce("tpc_y", raw_bytes, callback=lambda: print("Uploaded processed frame"))
        bytes_writer.flush()
        bytes_writer.close()


def start_parallel_consume(model: YoloObjectDetection, processes: int = 5):
    with Pool(processes) as p:
        p.map(consume, [model, ]*processes)

