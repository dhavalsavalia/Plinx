import sqlite3


class Database:
    def __init__(self, path: str):
        self.connection = sqlite3.Connection(path)

    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None

    @property
    def tables(self):
        return []
