from typing import Any


class Terminal:
    def __init__(self):
        pass

    @staticmethod
    def print(message: Any):
        print(f'> {message}')

    @staticmethod
    def empty():
        print('')
