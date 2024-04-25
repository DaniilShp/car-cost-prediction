import pandas as pd
import pymysql


class SQLDataLoader:
    def __init__(self):
        self.dataframe = None
        self.local_path = None

    def create_dataframe(self, dbconfig: dict, _sql: str, table_name: str):
        db_connection = pymysql.connect(**dbconfig)
        self.dataframe = pd.read_sql(_sql, con=db_connection)
        db_connection.close()
        self.local_path = f'data/dataframe_{table_name}.csv'
        self.dataframe.to_csv(self.local_path, index=False)
        return self.local_path

