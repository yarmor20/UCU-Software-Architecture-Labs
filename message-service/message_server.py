from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from __constants import *
from __utils import *


# Start FastAPI server.
app = FastAPI(title=str.capitalize(MESSAGE_SERVICE_NAME))


@app.exception_handler(Exception)
def exception_handler(request: Request, err):
    msg = f"Failed Method: [{request.method}] URL: [{request.url}].\nError: [{err}]"
    return JSONResponse(status_code=STATUS_ERROR, content={"message": msg})


@app.get("/message-svc/api/v1.0/get_messages", response_class=JSONResponse)
def get_messages(request: Request):
    response = json_response_template(status=STATUS_OK, msg="NOT IMPLEMENTED")
    return JSONResponse(content=response, status_code=STATUS_OK)


@app.post("/message-svc/api/v1.0/add_message")
def add_message():
    response = json_response_template(status=STATUS_ERROR, msg="NOT IMPLEMENTED")
    return JSONResponse(content=response, status_code=STATUS_ERROR)
