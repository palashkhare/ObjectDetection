from dataclasses import dataclass
from datetime import datetime
import io
import sys
from confluent_kafka import Producer, KafkaError
from avro.io import DatumWriter, BinaryEncoder
from avro import schema
import cv2


schema_path = "kafka/schema/frames.avsc"
kafka = Producer({"bootstrap.servers": "localhost:9092"})

# define a video capture object
vid = cv2.VideoCapture(0)

with open(schema_path, "r") as f:
    avro_schema = schema.parse(f.read())

with open("kafka/getting-started/documentation/cat_dog.jpg", "rb") as f:
    img = f.read()

writer = DatumWriter(avro_schema)


@dataclass
class Format:
    JPEG = "JPEG"
    ARRAY_3D = "ARRAY_3D"


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))


counter = 0

while True:
    # Capture the video frame
    # by frame
    t0 = datetime.now()
    kafka.poll(0)
    ret, frame = vid.read()

    data = {
        "uuid": f"frame_{counter}",
        "topic_id": "12345",
        "frame_id": counter,
        "frame_3d": frame.flatten().tobytes(),
        "format": Format.ARRAY_3D,
        "partition_id": 2,
    }

    bytes_writer = io.BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder=encoder)
    raw_bytes = bytes_writer.getvalue()
    kafka.produce("tpc_x", raw_bytes, callback=delivery_report)
    counter += 1
    bytes_writer.flush()
    bytes_writer.close()
    duration = (datetime.now() - t0).microseconds
    print(counter, " - Frames saved", 10**6/duration, " FPS")
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

kafka.flush()
