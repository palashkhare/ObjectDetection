from confluent_kafka.admin import AdminClient, NewTopic


config = {
    "bootstrap.servers": "localhost:9092"
}
admin_client = AdminClient(config)

topic_list = []
topic = NewTopic("example_topic", 1, 1)  # 1 replica, 1 partition
topic_list.append(topic)
admin_client.create_topics(topic_list)

print(admin_client.list_topics().topics)
