# ============== Microservices configs ==============
host="127.0.0.1"

# Logging Service.
consul kv put logging-service/api-root-path '/logging-service/api/v1.0'
consul kv put logging-service/get-msgs-endpoint '/get_messages'
consul kv put logging-service/add-msg-endpoint '/add_message'

# Message Service.
consul kv put message-service/api-root-path '/message-service/api/v1.0'
consul kv put message-service/get-msgs-endpoint '/get_messages'

# ============== Hazelcast configs ==============
hz_dir="hazelcast/"
consul kv delete -recurse "${hz_dir}hz-node-"

uuid1=$(uuidgen)
hazelcast_name1="${hz_dir}hz-node-${uuid1}"
consul kv put ${hazelcast_name1} "${host}:5701"

uuid2=$(uuidgen)
hazelcast_name2="${hz_dir}hz-node-${uuid2}"
consul kv put ${hazelcast_name2} "${host}:5702"

uuid3=$(uuidgen)
hazelcast_name3="${hz_dir}hz-node-${uuid3}"
consul kv put ${hazelcast_name3} "${host}:5703"

consul kv put hazelcast/hz-distributed-map 'lab5_distributed_map'


# ============== Kafka configs ==============
consul kv delete "kafka/kafka-broker"

kafka_broker_name="kafka/kafka-broker"
consul kv put ${kafka_broker_name} "${host}:9092"

consul kv put kafka/messages-svc-topic 'MessageServiceTopic'
consul kv put kafka/consumer-group 'MessageServiceConsumerGroup'