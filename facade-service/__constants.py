# Facade-Service (FS) constants.
FACADE_SERVICE_NAME = "facade-service"

# Multiple Message-Service URLs.
MESSAGE_SERVICE_URL_1 = 'http://localhost:8081/message-svc/api/v1.0'
MESSAGE_SERVICE_URL_2 = 'http://localhost:8082/message-svc/api/v1.0'

# Multiple Logging-Service Instances URLs.
LOGGING_SERVICE_URL_1 = 'http://localhost:8083/logging-svc/api/v1.0'
LOGGING_SERVICE_URL_2 = 'http://localhost:8084/logging-svc/api/v1.0'
LOGGING_SERVICE_URL_3 = 'http://localhost:8085/logging-svc/api/v1.0'

# Service Endpoints.
GET_MSGS_ENDPOINT = '/get_messages'
ADD_MSG_ENDPOINT = '/add_message'

# Kafka.
KAFKA_PRODUCER_NAME = "FacadeProducer"
KAFKA_BROKER = "127.0.0.1:9092"
MESSAGE_SERVICE_KAFKA_TOPIC = "MessageServiceTopic"

# Response statuses.
STATUS_OK = 200
STATUS_ERROR = 400
