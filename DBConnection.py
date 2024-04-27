from pymysql import connect
from pymysql.err import OperationalError


class DBContextManager:
    def __init__(self, config: dict):
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = connect(**self.config)
            self.cursor = self.connection.cursor()
            self.connection.begin()
            return self.cursor
        except OperationalError as err:
            print(err.args)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type:
            print(exc_type, exc_val)

        if self.cursor and self.connection:
            if exc_type:
                self.connection.rollback()
            else:
                self.connection.commit()

            self.cursor.close()
            self.connection.close()
        return True
