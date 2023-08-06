import sqlite3


class SQLite:
    """Manages the connection with the db.
    Attribution: https://tinyurl.com/5aph27bt"""
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.file_path)
        return self.conn.cursor()

    def __exit__(self, type_, value, traceback):
        if traceback is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
