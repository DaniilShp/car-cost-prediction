import requests
from bs4 import BeautifulSoup
import re
import colorama

colorama.init()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

class DromParser:
    def __init__(self, url_to_parse=None, user_agent_headers=None):
        if user_agent_headers is None:
            self.headers = headers
        else:
            self.headers = user_agent_headers
        if url_to_parse is not None:
            self.url_to_parse = url_to_parse
            self.page = requests.get(self.url_to_parse, headers=headers)
            if self.page.status_code != 200:
                raise ValueError(f"Failed to get data from given url, error: {self.page.status_code}")
            self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.result_dict = {}
    def __get_car_ids(self):
        self.car_hrefs = [el.get("href") for el in self.soup.find_all("a", class_="css-4zflqt e1huvdhj1")]
        if len(self.car_hrefs) != 0:
            print(self.car_hrefs)
        else:
            print(colorama.Fore.RED + "not found car_hrefs")
            print(colorama.Style.RESET_ALL)  # Сброс цветовых настроек
            return None
        self.car_ids = [int(el.split('/')[-1].split('.')[0]) for el in self.car_hrefs]
        return 0
    def __get_car_names_and_years(self):
        self.car_names_and_years = [el.text for el in self.soup.find_all("div", class_="css-16kqa8y e3f4v4l2")]
        if len(self.car_names_and_years) != 0:
            print(self.car_names_and_years)
            return 0
        else:
            print(colorama.Fore.RED + "not found car_names_and_years" + colorama.Style.RESET_ALL)
            return None
    def __get_car_specifications(self):
        spec = [el.text for el in self.soup.find_all("span", class_="css-1l9tp44 e162wx9x0")]
        self.car_specifications = [[spec[i + j] for i in range(5)] for j in range(0, len(spec), 5)]
        if len(self.car_specifications) != 0:
            print(self.car_specifications)
            return 0
        else:
            print(colorama.Fore.RED + "not found car_engine_specifications" + colorama.Style.RESET_ALL)
            return None
    def __get_car_prices(self):
        car_prices = [el.text for el in self.soup.find_all("span", class_="css-46itwz e162wx9x0")]
        self.car_prices = [int(''.join([sym for sym in word if sym.isdigit()])) for word in car_prices]
        if len(self.car_prices) != 0:
            print(self.car_prices)
            return 0
        else:
            print(colorama.Fore.RED + "not found car_prices" + colorama.Style.RESET_ALL)
            return None
    def format_data(self):
        if not (len(self.car_names_and_years)
                ==len(self.car_prices)
                ==len(self.car_ids)
                ==len(self.car_hrefs)
                ==len(self.car_specifications)):
            print(colorama.Fore.RED + "parsing fault occured: number of features doesn'match with number of cars")
            print(colorama.Style.RESET_ALL)  # Сброс цветовых настроек
            return None

        for i in range(len(self.car_ids)):
            name, year = self.car_names_and_years[i].split(', ')
            engine_volume, engine_power = re.findall(r'\d+\.\d+|\d+', self.car_specifications[i][0])
            self.result_dict[self.car_ids[i]] = \
                {"href": self.car_hrefs[i],
                 "name": name, "year": int(year),
                 "price": self.car_prices[i],
                 "volume": float(engine_volume),
                 "power": int(engine_power),
                 "gearbox_type": self.car_specifications[i][2].replace(',', ''),
                 #"wheel drive": int(self.car_specifications[i][3][0]),
                 "mileage": int(self.car_specifications[i][4].replace(' ', '').replace('км', ''))}
        print(self.result_dict)
        return 0
    def parse(self, change_url_to_parse=None):
        try:
            if change_url_to_parse is not None:
                self.__init__(url_to_parse=change_url_to_parse)
            if self.__get_car_ids() is None:
                return None
            if self.__get_car_names_and_years() is None:
                return None
            if self.__get_car_specifications() is None:
                return None
            if self.__get_car_prices() is None:
                return None
            if self.format_data() is None:
                return None
            print(colorama.Fore.GREEN + "page parsed successfully" + colorama.Style.RESET_ALL)
            return self.result_dict
        except IndexError:
            print(colorama.Fore.RED + "Index error" + colorama.Style.RESET_ALL)
            return None
        except ValueError:
            print(colorama.Fore.RED + "Value error" + colorama.Style.RESET_ALL)
            return None

