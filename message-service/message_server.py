from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from message_consumer import consume_messages, MESSAGES_MAP
from __constants import *
from __utils import *
import asyncio
import consul


# Start FastAPI server.
app = FastAPI(title=str.capitalize(MESSAGE_SERVICE_NAME))

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

# Start Kafka consumer asynchronously.
asyncio.create_task(consume_messages(cclient))


@app.exception_handler(Exception)
def exception_handler(request: Request, err):
    msg = f"Failed Method: [{request.method}] URL: [{request.url}]. Error: [{err}]"
    return JSONResponse(status_code=STATUS_ERROR, content={"message": msg})


@app.get("/message-service/api/v1.0/get_messages", response_class=JSONResponse)
def get_messages():
    """
    Get all messages from the in-memory map.

    :return: (JSONResponse) - response status and all messages in response body.
    """
    messages = list(MESSAGES_MAP.values())
    response = json_response_template(status=STATUS_OK, msg=", ".join(messages))
    return JSONResponse(content=response, status_code=STATUS_OK)


@app.on_event("shutdown")
def shutdown_event():
    print("(CONSUL) This service is being deregistered...")
    cclient.agent.service.deregister(SERVICE_ID)
