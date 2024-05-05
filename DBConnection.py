from sqlalchemy import create_engine, text, insert, Table, Column, MetaData, Integer, String, Numeric
from sqlalchemy.exc import IntegrityError
import json
from functools import lru_cache


@lru_cache(maxsize=1)
def create_table_structure(table_name):
    metadata = MetaData()
    my_table = Table(table_name, metadata,
                     Column('car_id', Integer, primary_key=True),
                     Column('brand_model', String(30)),
                     Column('mileage', Integer),
                     Column('gearbox_type', String(30)),
                     Column('power', Integer),
                     Column('price', Integer),
                     Column('volume', Numeric(precision=2, scale=1)),
                     Column('href', String(80)),
                     Column('production_year', Integer))
    metadata.create_all(mysql_engine)
    return my_table


class GetDBConfig:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.dbconfig = json.load(f)

    @property
    def database_urL_pymysql(self):
        # mysql+pymysql://username:password@localhost/db_name
        return 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(**self.dbconfig)


def select(engine, table_name, query):
    create_table_structure(table_name)
    with engine.connect() as conn:
        cursor = conn.execute(text(query))
    return cursor


def insert_data(engine, table_name, values_dict):
    my_table = create_table_structure(table_name)
    with engine.connect() as conn:
        for values in values_dict:
            try:
                conn.execute(insert(my_table).values(values))
            except IntegrityError as err:
                print(err)
        conn.commit()


dbconfig = GetDBConfig('configs/dbconfig.json')
mysql_engine = create_engine(url=dbconfig.database_urL_pymysql)
