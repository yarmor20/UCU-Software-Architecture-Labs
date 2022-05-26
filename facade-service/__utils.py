from pydantic import BaseModel


class Message(BaseModel):
    message: str


def json_response_template(status: int, msg: str):
    return {
        "_status_code": status,
        "response": msg
    }


def json_response_msg_template(component, status, msg):
    return f"""
    Response Component: [{component}]
    \tStatus: [{status}]
    \tResponse: [{msg}]\n
    """
