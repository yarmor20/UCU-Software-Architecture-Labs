import dotenv
import uuid
import os


# Load dotenv.
dotenv.load_dotenv(dotenv_path="./logging-service.env")

# Service identifier variables.
SERVICE_HOST = os.getenv("HOST")
SERVICE_PORT = int(os.getenv("PORT"))
SERVICE_NAME = "logging-service"
SERVICE_ID = f"{SERVICE_NAME}-{uuid.uuid1().__str__()}"

# Facade-Service (FS) constants.
LOGGING_SERVICE_NAME = "logging-service"

# Consul.
CONSUL_CLIENT_HOST = "127.0.0.1"
CONSUL_CLIENT_PORT = 8500

# Consul KV Keys.
HAZELCAST_NODE_ADDRESSES_KEY = "hazelcast/hz-node"
HAZELCAST_DISTRIBUTED_MAP_NAME_KEY = "hazelcast/hz-distributed-map"

# Response statuses.
STATUS_OK = 200
STATUS_ERROR = 400
