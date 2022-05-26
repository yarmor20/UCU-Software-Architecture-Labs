from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from __constants import *
from __logger import logger
from __utils import *


# Start FastAPI server.
app = FastAPI(title=str.capitalize(LOGGING_SERVICE_NAME))
MESSAGES_MAP = dict()


@app.exception_handler(Exception)
def exception_handler(request: Request, err):
    msg = f"Failed Method: [{request.method}] URL: [{request.url}].\nError: [{err}]"
    return JSONResponse(status_code=STATUS_ERROR, content={"message": msg})


@app.get("/logging-svc/api/v1.0/get_messages", response_class=JSONResponse)
async def get_messages(request: Request):
    """
    Get all messages from the in-memory map.

    :return: (JSONResponse) - response status and all messages in response body.
    """
    messages = list(MESSAGES_MAP.values())
    response = json_response_template(status=STATUS_OK, msg=", ".join(messages))
    return JSONResponse(content=response, status_code=STATUS_OK)


@app.post("/logging-svc/api/v1.0/add_message")
async def add_message(msg: dict):
    """
    Add a message to the global in-memory map.

    :param msg: (dict) - pair of message uuid and message itself.
    :return: (JSONResponse) - response status.
    """
    # Insert message into a dict.
    uuid, msg = list(msg.items())[0]
    MESSAGES_MAP[uuid] = msg

    logger.info(f"(LOGGING) Message received: [{msg}]")

    response = json_response_template(status=STATUS_OK, msg="OK")
    return JSONResponse(content=response, status_code=STATUS_OK)
