from fastapi.responses import JSONResponse
from __kafka_producer import ServiceProducer
from __logger import logger
from __utils import *
from __constants import *

import uuid
import httpx
import asyncio
import random


async def get(client: httpx.AsyncClient, url: str) -> dict:
    """
    Async GET request.

    :param client: (httpx.AsyncClient) - async client.
    :param url: (str) - request URL.
    :return: (dict) - response body.
    """
    response = await client.get(url)
    logger.info(f"(FACADE) Request: [GET] Response Body: [{response.json()}]")
    return response.json()


async def post(client: httpx.AsyncClient, url: str, msg: dict) -> dict:
    """
    Async POST request.

    :param client: (httpx.AsyncClient) - async client.
    :param url: (str) - request URL.
    :param msg: (dict) - json object.
    :return: (dict) - response body.
    """
    response = await client.post(url, json=msg)
    logger.info(f"(FACADE) Request: [POST] Response Body: [{response.json()}]")
    return response.json()


async def _get_messages() -> JSONResponse:
    """
    Get all messages from Logging-Service (LS).
    Send also GET request to Message-Service (MS).

    :return: (JSONResponse) - concatenated responses from LS and MS.
    """
    # Get random url for logging & message services.
    logging_service_url = random.choice([LOGGING_SERVICE_URL_1, LOGGING_SERVICE_URL_2, LOGGING_SERVICE_URL_3])
    logging_service_url += GET_MSGS_ENDPOINT

    message_service_url = random.choice([MESSAGE_SERVICE_URL_1, MESSAGE_SERVICE_URL_2])
    message_service_url += GET_MSGS_ENDPOINT

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


async def __add_logging_service_message(msg: str) -> dict:
    """
    Send a message via Logging-Service endpoint.

    :param msg: (str) - message to be sent.
    :return: (dict) - server response.
    """
    # Get logging service url.
    logging_service_url = random.choice([LOGGING_SERVICE_URL_1, LOGGING_SERVICE_URL_2, LOGGING_SERVICE_URL_3])
    logging_service_url += ADD_MSG_ENDPOINT

    # Send async POST request.
    try:
        async with httpx.AsyncClient() as client:
            tasks = [post(client, url=logging_service_url, msg={uuid.uuid1().__str__(): msg})]
            responses = await asyncio.gather(*tasks)
    except Exception as err:
        responses = [{"_status_code": STATUS_ERROR, "error": err}]

    logger.info(f"(FACADE->LOGGING) Request: [POST] Response Body: [{responses[0]}]")
    return responses


async def __add_message_service_message(msg: str) -> int:
    """
    Send a message via Kafka producer to the target Kafka topic.

    :param msg: (str) - message to be sent.
    :return: (int) - status code.
    """
    try:
        # Create a Kafka producer instance to send message to kafka topic.
        producer = ServiceProducer(logger_name=KAFKA_PRODUCER_NAME, broker=KAFKA_BROKER)

        # Send a message to the topic, which is read by consumer group from Message service side
        await producer.send(topic=MESSAGE_SERVICE_KAFKA_TOPIC, message={"message": msg})
        return STATUS_OK
    except Exception as err:
        logger.error(f"(FACADE->MESSAGE) Failed to send message via Kafka Producer. Error: [{err}]")
        return STATUS_ERROR


async def _add_message(msg: str) -> JSONResponse:
    """
    Send message to both Logging-Service and Message-Service.

    :param msg: (str) - message to be sent.
    :return: (JSONResponse) - responses from LS and MS.
    """
    # Add message to both logging and message services.
    log_svc_response = await __add_logging_service_message(msg)
    msg_svc_response = await __add_message_service_message(msg)

    if log_svc_response[0]["_status_code"] == STATUS_OK and msg_svc_response == STATUS_OK:
        status = STATUS_OK
        response = json_response_template(status=status, msg="(FACADE->ALL) OK")
    else:
        status = STATUS_ERROR
        error_message = str(log_svc_response[0]["error"]) if log_svc_response[0].get("error", None) else "ERROR"
        response = json_response_template(status=status, msg=f"(FACADE->ALL) Internal server error: [{error_message}]")
    return JSONResponse(content=response, status_code=status)
