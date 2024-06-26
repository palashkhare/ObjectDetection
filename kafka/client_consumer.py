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

c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'Client Consumer',
        'auto.offset.reset': 'earliest'
    })


schema_path = "kafka/schema/frames.avsc"

with open(schema_path, "r") as f:
    avro_schema = schema.parse(f.read())


reader = DatumReader(avro_schema)

c.subscribe(['tpc_y'])

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
    bytes_reader.flush()
    bytes_reader.close()

    cv2.imshow('frame', frame) 

    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
