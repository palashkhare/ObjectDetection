from confluent_kafka.admin import AdminClient, NewTopic

kafka = AdminClient({'bootstrap.servers': 'localhost:9092'})

topic = ["topic1", "topic2"]
create_topics = []

for t in topic:
    create_topics.append(
        NewTopic(t, num_partitions=2, replication_factor=1)
    )
# Note: In a multi-cluster production scenario, it is more typical 
# to use a replication_factor of 3 for durability.

# Call create_topics to asynchronously create topics. A dict
# of <topic,future> is returned.
fs = kafka.create_topics(create_topics)

# Wait for each operation to finish.
for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))