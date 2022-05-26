from fastapi.responses import JSONResponse
from __logger import logger
from __utils import *
from __constants import *

import uuid
import httpx
import asyncio
import random


async def get(client: httpx.AsyncClient, url: str):
    response = await client.get(url)
    response = response.json()

    logger.info(f"(FACADE) Request: [GET] Response Body: [{response}]")
    return response


async def post(client: httpx.AsyncClient, url: str, msg: dict):
    response = await client.post(url, json=msg)
    response = response.json()

    logger.info(f"(FACADE) Request: [POST] Response Body: [{response}]")
    return response.json()


async def _get_messages():
    """
    Get all messages from Logging-Service (LS).
    Send also GET request to Message-Service (MS).

    :return: (JSONResponse) - concatenated responses from LS and MS.
    """
    # Get all urls for logging & message services.
    logging_service_url = random.choice([LOGGING_SERVICE_URL_1, LOGGING_SERVICE_URL_2, LOGGING_SERVICE_URL_3])
    logging_service_url = logging_service_url + LOGGING_SERVICE_GET_MSGS_ENDPOINT
    message_service_url = MESSAGE_SERVICE_URL + MESSAGE_SERVICE_GET_MSGS_ENDPOINT

    # Send async GET request to microservices.
    try:
        async with httpx.AsyncClient() as client:
            tasks = [get(client, url=logging_service_url), get(client, url=message_service_url)]
            responses = await asyncio.gather(*tasks)
    except Exception as err:
        responses = [{"component": "UNKNOWN", "_status_code": STATUS_ERROR, "response": {}, "error": err}]

    # Return both responses to user in a concatenated form.
    final_response_message = ""
    for response in responses:
        if response["_status_code"] != STATUS_OK:
            # Compose JSON Response failure message.
            component, msg = response["component"], str(response["error"]) if response.get("error", None) else "ERROR"
            json_message = json_response_msg_template(component=component, status=STATUS_ERROR, msg=msg)
            # Return JSON Response.
            json_response = json_response_template(status=STATUS_ERROR, msg=json_message)
            return JSONResponse(content=json_response, status_code=STATUS_ERROR)

        # Save the response.
        component, msg = response["component"], response["response"]
        final_response_message += json_response_msg_template(component=component, status=STATUS_OK, msg=msg)

    # Return concatenated JSON Response.
    response = json_response_template(status=STATUS_OK, msg=final_response_message)
    return JSONResponse(content=response, status_code=STATUS_OK)


async def _add_message(msg: str):
    # Get logging service url.
    logging_service_url = random.choice([LOGGING_SERVICE_URL_1, LOGGING_SERVICE_URL_2, LOGGING_SERVICE_URL_3])
    url = logging_service_url + LOGGING_SERVICE_ADD_MSG_ENDPOINT

    # Send async POST request.
    try:
        async with httpx.AsyncClient() as client:
            tasks = [post(client, url=url, msg={uuid.uuid1().__str__(): msg})]
            responses = await asyncio.gather(*tasks)
    except Exception as err:
        responses = [{"_status_code": STATUS_ERROR, "error": err}]

    if responses[0]["_status_code"] == STATUS_OK:
        response = json_response_template(status=STATUS_OK, msg="OK")
    else:
        response = json_response_template(status=STATUS_ERROR, msg="ERROR")

    logger.info(f"(FACADE->LOGGING) Request: [POST] Response Body: [{response}]")
    return JSONResponse(status_code=STATUS_OK, content=response)
