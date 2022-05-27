import dotenv
import uuid
import os


# Load dotenv.
dotenv.load_dotenv(dotenv_path="./message-service.env")

# Service identifier variables.
SERVICE_HOST = os.getenv("HOST")
SERVICE_PORT = int(os.getenv("PORT"))
SERVICE_NAME = "message-service"
SERVICE_ID = f"{SERVICE_NAME}-{uuid.uuid1().__str__()}"

# Consul.
CONSUL_CLIENT_HOST = "127.0.0.1"
CONSUL_CLIENT_PORT = 8500

# Consul KV Keys.
KAFKA_CONSUMER_GROUP_KEY = "kafka/consumer-group"
KAFKA_BROKER_KEY = "kafka/kafka-broker"
MESSAGE_SERVICE_KAFKA_TOPIC_KEY = "kafka/messages-svc-topic"

# Facade-Service (FS) constants.
MESSAGE_SERVICE_NAME = "message-service"

# Response statuses.
STATUS_OK = 200
STATUS_ERROR = 400
