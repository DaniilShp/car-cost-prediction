from get_data_samples import DromParser
from sql_provider import SQLProvider
from work_with_db import insert_dict, select_dict
import os
import json

car_brand = "audi"
db_table = "audi_cars"
home_url = "https://auto.drom.ru"
settings_url = "mv=0.1&pts=2&damaged=2&unsold=1&minpower=1&minprobeg=1"

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
with open('dbconfig.json') as f:
    dbconfig = json.load(f)

data_samples_amount = select_dict(dbconfig, f"select count(car_id) as samples_amount from {db_table}")
print("data samples exists: ", data_samples_amount[0]["samples_amount"])


if __name__ == '__main__':
    parser = DromParser()
    for page in range(1, 101):
        print(page)
        result_dicts = parser.parse(change_url_to_parse=f"{home_url}/{car_brand}/page{page}/?{settings_url}")
        if result_dicts is None:
            continue
        for dict in result_dicts.values():
            dict["table"] = db_table
        _sql = [provider.get('insert_data_samples.sql', **result_dict) for result_dict in result_dicts.values()]
        insert_dict(dbconfig, *_sql)
    new_rows_amount = select_dict(dbconfig, f"select count(car_id) as samples_amount from {db_table}")
    print("new data samples found: ", new_rows_amount[0]["samples_amount"] - data_samples_amount[0]["samples_amount"])
