from get_data_samples import DromParser

car_brand = "lada"
home_url = "https://auto.drom.ru"
settings_url = "mv=0.1&pts=2&damaged=2&unsold=1&minpower=1&minprobeg=1"

if __name__ == '__main__':
    parser = DromParser()
    for page in range(100):
        print(page)
        result = parser.parse(change_url_to_parse=f"{home_url}/{car_brand}/page{page}/?{settings_url}")
        if result is None:
            continue