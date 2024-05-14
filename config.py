import os
import json

_ASYNC = False  # async parsing mode enable (server can sometimes return 503 error code, but faster x5)

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

dbconfig_path = os.path.join(current_dir, 'configs', 'dbconfig.json')
parseconfig_path = os.path.join(current_dir, 'configs', 'parseconfig_toyota_cars.json')
regression_model_config_path = os.path.join(current_dir, 'configs', 'regression_model_config.json')

with open(dbconfig_path, 'r') as f:
    _dbconfig = json.load(f)
with open(parseconfig_path, 'r') as f:
    _parseconfig = json.load(f)
with open(regression_model_config_path, 'r') as f:
    _regression_model_config = json.load(f)

_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
}
