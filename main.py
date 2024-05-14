import asyncio
import time
from parsing.drom_parser import AsyncDromParser, SyncDromParser
from work_with_db.sql_provider import SQLProvider
from typing import Any
import pandas as pd
import os
import json
from regression.linear_regression_model import linear_regression_create
from regression.polynomial_regression_model import polynomial_regression_create
from regression.random_forest_regression import random_forest_regression_create
#from regression.fully_connected_neural_network_model import FullyConnectedNeuralNetwork
from work_with_db.db_queries import insert_dict, select_dict
from work_with_db.db_connection import DBConnectionError
from work_with_db.sql_to_csv import SQLDataLoader
import colorama

colorama.init()
ASYNC = False
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

with open('configs/dbconfig.json') as f:
    dbconfig = json.load(f)
with open('configs/parseconfig_toyota_cars.json', 'r') as f:
    parseconfig = json.load(f)
with open('configs/regression_model_config.json', 'r') as f:
    regression_model_config = json.load(f)


def parse_pages(db_config: dict, parse_config: dict, parser: Any):
    _parse_config = parse_config
    _parser = parser()
    _db_config = db_config

    def inner(pages_range: range):
        try:
            data_samples_amount = select_dict(dbconfig, "select count(car_id) as samples_amount from {db_table}".format(
                **_parse_config))
        except DBConnectionError:
            print(colorama.Fore.RED + "failed to connect to the DB" + colorama.Style.RESET_ALL)
            return None
        for page in pages_range:
            result_dicts = _parser.parse(
                change_url_to_parse=
                f"{_parse_config['home_url']}/{_parse_config['car_brand']}/page{page}/{_parse_config['settings_url']}")
            print(page)
            if result_dicts is None:
                continue
            for _dict in result_dicts:
                _dict["table"] = _parse_config["db_table"]
            _sql = [provider.get('insert_data_samples.sql', **result_dict) for result_dict in result_dicts]
            try:
                insert_dict(_db_config, *_sql)
            except DBConnectionError:
                print(colorama.Fore.RED + "failed to connect to the DB" + colorama.Style.RESET_ALL)
                return

        new_rows_amount = select_dict(dbconfig,
                                      "select count(car_id) as samples_amount from {db_table}".format(**_parse_config))
        print("new data samples found: ",
              new_rows_amount[0]["samples_amount"] - data_samples_amount[0]["samples_amount"])
        print("data samples now exists: ", new_rows_amount[0]["samples_amount"])

    return inner


async def parse_page(db_config: dict, parse_config: dict, parser: Any, page: int):
    _parser = parser()
    await _parser.parse(
        change_url_to_parse=
        f"{parse_config['home_url']}/{parse_config['car_brand']}/page{page}/{parse_config['settings_url']}")
    print(page)
    if _parser.resulting_dicts is None:
        return None
    for _dict in _parser.resulting_dicts:
        _dict["table"] = parse_config["db_table"]
    _sql = [provider.get('insert_data_samples.sql', **result_dict) for result_dict in _parser.resulting_dicts]
    try:
        insert_dict(db_config, *_sql)
    except DBConnectionError:
        print(colorama.Fore.RED + "failed to connect to the DB" + colorama.Style.RESET_ALL)
        return None


async def async_parse_pages(db_config: dict, parse_config: dict, parser: Any, pages_range: range):
    _parse_config = parse_config
    _db_config = db_config
    tasks = [parse_page(_db_config, _parse_config, parser, page) for page in pages_range]
    task_list = [asyncio.create_task(task) for task in tasks]
    try:
        data_samples_amount = select_dict(dbconfig, "select count(car_id) as samples_amount from {db_table}".format(
            **_parse_config))
    except DBConnectionError:
        print(colorama.Fore.RED + "failed to connect to the DB" + colorama.Style.RESET_ALL)
        return None
    await asyncio.gather(*task_list)
    new_rows_amount = select_dict(dbconfig,
                                  "select count(car_id) as samples_amount from {db_table}".format(**_parse_config))
    print("new data samples found: ",
          new_rows_amount[0]["samples_amount"] - data_samples_amount[0]["samples_amount"])
    print("data samples now exists: ", new_rows_amount[0]["samples_amount"])


if __name__ == '__main__':
    print("Would you like to update dataframe with samples? (y/n)")
    answer = input()

    """__________________ PARSING AND UPDATING DB __________________"""
    if answer == "y" or answer == "Y":

        time_start = time.time()

        if ASYNC:
            parse_params = (dbconfig, parseconfig, AsyncDromParser,
                            range(parseconfig["page_range_start"],
                                  parseconfig["page_range_stop"]))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(async_parse_pages(*parse_params))
        else:
            parse_toyota_cars = parse_pages(dbconfig, parseconfig, SyncDromParser)
            parse_toyota_cars(pages_range=range(parseconfig["page_range_start"], parseconfig["page_range_stop"]))

        print(f"time left: {time.time() - time_start}")

    print("Would you like to update csv_file with samples? (y/n)")
    answer = input()

    """_________ CREATING (UPDATING) CSV FILE WITH SAMPLES _________"""
    if answer == "y" or answer == "Y":
        data_loader = SQLDataLoader()
        db_table = parseconfig['db_table']
        local_path = data_loader.create_dataframe(dbconfig, f"select * from {db_table}", db_table)
        dataframe = pd.read_csv(local_path)
    else:
        dataframe = pd.read_csv(regression_model_config['csv_dataframe_filename'])

    """______________ CREATING LINEAR REGRESSION MODEL ______________"""
    x = dataframe[["production_year", "volume", "power", "mileage", "brand_model", "gearbox_type"]]
    y = dataframe["price"]
    linear_regression_create(x, y)
    """____________ CREATING POLYNOMIAL REGRESSION MODEL ____________"""
    x, y = dataframe[["volume", "power", "mileage", "production_year"]], dataframe["price"]
    polynomial_regression_create(x, y, degree=3)
    """____________ CREATING POLYNOMIAL REGRESSION MODEL ____________"""
    x = dataframe[["production_year", "volume", "power", "mileage", "brand_model", "gearbox_type"]]
    random_forest_regression_create(x, y)
    """_____________ CREATING FEEDFORWARD NEURAL NETWORK ____________"""
    x, y = dataframe[["volume", "power", "mileage", "production_year"]], dataframe["price"]
    model = FullyConnectedNeuralNetwork(input_size=(x.shape[1],))
    x_train, x_test, y_train, y_test = model.train_test_split(x, y, test_size=0.2, random_state=1)
    x_train, x_test = model.normalize_data(x_train), model.normalize_data(x_test)
    try:
        model.load_model(regression_model_config['neural_model_fitted_filename'])
        print("model has been loaded successfully")
    except (FileNotFoundError, OSError):
        print("Prepared model hasn't been found. Wait for model fitting, or change regression_model_config.json")
        model.fit(x_train, y_train, **regression_model_config)
    y_pred = model.predict(x_test)
    model.print_error_metrics(y_test, y_pred, scatterplot=True, barplot=True, title="Нейронная сеть")
