class OperatorException(Exception):
    def __init__(self, message, status = 1):
        super().__init__(message)
        self.status = status