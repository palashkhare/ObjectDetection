from confluent_kafka import Producer

kafka = Producer({'bootstrap.servers': 'localhost:9092'})
with open("kafka-server/getting-started/documentation/cat_dog.jpg", "rb") as f:
    some_data_source = ["Hello", f.read()]


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(
            msg.topic(), msg.partition()
        ))


for data in some_data_source:
    # Trigger any available delivery report callbacks from previous
    # produce() calls
    kafka.poll(0)

    # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    kafka.produce('topic1', data, callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
kafka.flush()