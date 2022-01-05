class UnauthorizedAccessException(Exception):
    message: str

    def __init__(self, message: str = "Unauthorized"):
        self.message = message
