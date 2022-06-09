import base64
from dataclasses import dataclass


class Logger:
    def info(self, message: str):
        ...


class UserData:
    model = None


@dataclass
class Response:
    body: str
    headers: dict
    content_type: str
    status_code: int


class Context:
    logger = Logger()
    user_data = UserData()
    Response = Response


class Event:
    def __init__(self, image_path: str, threshold: float):
        """
        Create an event with the image body serialised as base64
        """
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("ascii")
            self.body = {
                "image": image_base64,
                "threshold": threshold,
            }
