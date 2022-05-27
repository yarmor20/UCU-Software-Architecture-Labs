import dotenv
import uuid
import os


# Load dotenv.
dotenv.load_dotenv(dotenv_path="./facade-service.env")

# Service identifier variables.
SERVICE_HOST = os.getenv("HOST")
SERVICE_PORT = int(os.getenv("PORT"))
SERVICE_NAME = "facade-service"
SERVICE_ID = f"{SERVICE_NAME}-{uuid.uuid1().__str__()}"

# Other service names.
FACADE_SERVICE_NAME = "facade-service"
LOGGING_SERVICE_NAME = "logging-service"
MESSAGE_SERVICE_NAME = "message-service"

# Consul.
CONSUL_CLIENT_HOST = "127.0.0.1"
CONSUL_CLIENT_PORT = 8500

# Consul KV Keys.
LOGGING_SERVICE_API_ROOT_ENDPOINT_KEY = "logging-service/api-root-path"
LOGGING_SERVICE_GET_MSGS_ENDPOINT_KEY = "logging-service/get-msgs-endpoint"
LOGGING_SERVICE_ADD_MSG_ENDPOINT_KEY = "logging-service/add-msg-endpoint"

MESSAGE_SERVICE_API_ROOT_ENDPOINT_KEY = "message-service/api-root-path"
MESSAGE_SERVICE_GET_MSGS_ENDPOINT_KEY = "message-service/get-msgs-endpoint"

KAFKA_BROKER_KEY = "kafka/kafka-broker"
MESSAGE_SERVICE_KAFKA_TOPIC_KEY = "kafka/messages-svc-topic"

# Kafka.
KAFKA_PRODUCER_NAME = "FacadeProducer"

# Response statuses.
STATUS_OK = 200
STATUS_ERROR = 400
