class BadRequestPayload(Exception):
    def __init__(self, response_message: str):
        self.response_message = response_message
