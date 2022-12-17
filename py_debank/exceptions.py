from typing import Optional


class DebankException(Exception):
    def __init__(self, status_code: int, error_msg: Optional[str] = None):
        self.status_code: int = status_code
        self.error_msg: Optional[str] = error_msg

    def __str__(self):
        return f'Status code: {self.status_code}, Error message: {self.error_msg}'
