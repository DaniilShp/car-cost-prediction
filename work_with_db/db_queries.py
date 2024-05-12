from work_with_db.db_connection import DBContextManager, DBConnectionError
import pymysql


def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise DBConnectionError("Курсор не создан")
        else:
            cursor.execute(_sql)
            products = cursor.fetchall()
            if products:
                schema = [item[0] for item in cursor.description]
                products_dict = []
                for product in products:
                    products_dict.append(dict(zip(schema, product)))
                return products_dict
            else:
                return None


def insert_dict(db_config: dict, *query_list):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise DBConnectionError("Курсор не создан")
        else:
            for query in query_list:
                try:
                    cursor.execute(query)
                except pymysql.err.IntegrityError as err:
                    print(err)
