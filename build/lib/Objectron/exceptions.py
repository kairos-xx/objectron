class TransformationError(Exception):
    """
    Exception raised when an error occurs during object transformation.
    """

    def __init__(self, message: str):
        super().__init__(message)
