from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from facade import _add_message, _get_messages
from __constants import *
from __utils import *


# Start FastAPI server.
app = FastAPI(title=str.capitalize(FACADE_SERVICE_NAME))


@app.exception_handler(Exception)
def exception_handler(request: Request, err):
    msg = f"Failed Method: [{request.method}] URL: [{request.url}].\nError: [{err}]"
    return JSONResponse(status_code=STATUS_ERROR, content={"message": msg})


@app.get('/get_messages', response_class=JSONResponse)
async def get_messages():
    """
    Get all messages from Logging-Service (LS).
    Send also GET request to Message-Service (MS).

    :return: (JSONResponse) - concatenated responses from LS and MS.
    """
    return await _get_messages()


@app.post('/add_message')
async def add_message(msg: Message):
    """
    Send message to Logging-Service (LS) to be stored there.

    :param msg: (Message(str)) - message to be sent to LS.
    :return: (JSONResponse) - response status.
    """
    return await _add_message(msg.message)
