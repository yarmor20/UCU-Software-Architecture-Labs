from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from __constants import *
from __logger import logger
from __utils import *
import hazelcast
import consul


# Start FastAPI server.
app = FastAPI(title=str.capitalize(LOGGING_SERVICE_NAME))

# Configure Consul agent client.
cclient = consul.Consul(
    host=CONSUL_CLIENT_HOST,
    port=CONSUL_CLIENT_PORT
)

# Register a new instance of service in Consul.
cclient.agent.service.register(
    name=SERVICE_NAME,
    service_id=SERVICE_ID,
    address=SERVICE_HOST,
    port=SERVICE_PORT
)

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster.
hzclient = hazelcast.HazelcastClient(cluster_members=get_service_urls(cclient, HAZELCAST_NODE_ADDRESSES_KEY))
MESSAGES_MAP = hzclient.get_map(get_consul_value(cclient, key=HAZELCAST_DISTRIBUTED_MAP_NAME_KEY)).blocking()


@app.exception_handler(Exception)
def exception_handler(request: Request, err):
    msg = f"Failed Method: [{request.method}] URL: [{request.url}].\nError: [{err}]"
    return JSONResponse(status_code=STATUS_ERROR, content={"message": msg})


@app.get("/logging-service/api/v1.0/get_messages", response_class=JSONResponse)
async def get_messages():
    """
    Get all messages from the in-memory map.

    :return: (JSONResponse) - response status and all messages in response body.
    """
    messages = list(MESSAGES_MAP.values())
    response = json_response_template(status=STATUS_OK, msg=", ".join(messages))
    return JSONResponse(content=response, status_code=STATUS_OK)


@app.post("/logging-service/api/v1.0/add_message")
async def add_message(msg: dict):
    """
    Add a message to the global in-memory map.

    :param msg: (dict) - pair of message uuid and message itself.
    :return: (JSONResponse) - response status.
    """
    # Insert message into a dict.
    uuid_, msg = list(msg.items())[0]
    MESSAGES_MAP.put(uuid_, msg)

    logger.info(f"(LOGGING) Message received: [{msg}]")

    response = json_response_template(status=STATUS_OK, msg="OK")
    return JSONResponse(content=response, status_code=STATUS_OK)


@app.on_event("shutdown")
def shutdown_event():
    print("(CONSUL) This service is being deregistered...")
    cclient.agent.service.deregister(SERVICE_ID)
