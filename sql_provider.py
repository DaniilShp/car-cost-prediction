
import os
from string import Template


class SQLProvider:
    def __init__(self, file_path: str):
        self._scripts = {}
        for file in os.listdir(file_path): # file = product.sql, а не file_path/file
            sql = open(f'{file_path}/{file}').read()
            self._scripts[file] = Template(sql)

    def get(self, name, **kwargs):
        sql = self._scripts[name].substitute(**kwargs)
        return sql
