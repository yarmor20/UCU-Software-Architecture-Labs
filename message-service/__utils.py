def json_response_template(status: int, msg: str) -> dict:
    """
    Template for JSONResponse content.

    :param status: (int) - response status.
    :param msg: (str) - response message.
    :return: (dict) - json object, content.
    """
    return {
        "component": "message-service",
        "_status_code": status,
        "response": msg
    }


def json_response_msg_template(component: str, status: int, msg: str) -> str:
    """
    Template for extended response message.

    :param component: (str) - service name.
    :param status: (int) - response status.
    :param msg: (str) - some message.
    :return: (str) - message.
    """
    return f"""
    Response Component: [{component}]
    Status: [{status}]
    Response: [{msg}]
    """


def get_consul_value(client, key: str):
    """
    Get value from Consul value by key.

    :param client: (consul.Consul) - Consul agent client.
    :param key: (str) - key that is in KV storage.
    :return: (str) - value from KV storage.
    """
    index, data = client.kv.get(key, index=None)
    return data["Value"].decode("utf-8") if data else None
