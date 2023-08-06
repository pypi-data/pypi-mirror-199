import random
import requests
from .country import Country
from account_generator_helper.countries import Counties
from typing import List

from ..exceptions import NoCountyFound

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}


class Receive:
    def __init__(self, proxy):
        self._s = requests.Session()
        if proxy:
            self._s.proxies.update({'http': proxy, 'https': proxy})
        self._s.headers.update(headers)
        self._countries = dict()

    def get_counties(self) -> List[Country]:
        """
        :return: List of counties.
        """
        pass

    def get_country(self, phone_country: Counties) -> Country:
        """
        Method returns object of the country, from this object you can get the phone number of this country.

        :param phone_country: Country.
        :return: Country object.
        """
        if not self._countries:
            self.get_counties()
        result = self._countries.get(phone_country, None)
        if not result:
            raise NoCountyFound()

        return result

    def get_random_country(self) -> Country:
        """
        :return: Random Country object.
        """
        return random.choice(self.get_counties())

    def __repr__(self):
        return '(Receive country_count={})'.format(len(self._countries))
