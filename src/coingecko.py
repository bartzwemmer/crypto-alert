import json

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CoinGeckoAPI:
    __API_URL_BASE = "https://api.coingecko.com/api/v3/"
    __PRO_API_URL_BASE = "https://pro-api.coingecko.com/api/v3/"

    def __init__(self, api_key: str = "", retries=5, demo_api_key: str = ""):

        self.extra_params = None
        # self.headers = None
        if api_key:
            self.api_base_url = self.__PRO_API_URL_BASE
            self.extra_params = {"x_cg_pro_api_key": api_key}
            # self.headers = {"accept": "application/json",
            #                 "x-cg-pro-api-key": api_key}
        else:
            self.api_base_url = self.__API_URL_BASE
            if demo_api_key:
                self.extra_params = {"x_cg_demo_api_key": demo_api_key}
                # self.headers = {"accept": "application/json",
                #                 "x-cg-demo-api-key": demo_api_key}

        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(
            total=retries, backoff_factor=0.5, status_forcelist=[502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def __request(self, url, params):
        # if using pro or demo version of CoinGecko with api key, inject key in every call
        if self.extra_params is not None:
            params.update(self.extra_params)

        try:
            response = self.session.get(
                url, params=params, timeout=self.request_timeout
            )
        except requests.exceptions.RequestException:
            raise

        try:
            response.raise_for_status()
            # self._headers = response.headers
            content = json.loads(response.content.decode("utf-8"))
            return content
        except Exception as e:
            # check if json (with error message) is returned
            try:
                content = json.loads(response.content.decode("utf-8"))
                raise ValueError(content)
            # if no json
            except json.decoder.JSONDecodeError:
                pass

            raise

    def get_coin_market_chart_by_id(self, id, vs_currency, days, **kwargs):
        """Get historical market data include price, market cap, and 24h volume (granularity auto)"""

        # api_url = '{0}coins/{1}/market_chart?vs_currency={2}&days={3}'.format(self.api_base_url, id, vs_currency, days)
        # api_url = self.__api_url_params(api_url, kwargs, api_url_has_params=True)
        api_url = "{0}coins/{1}/market_chart".format(
            self.api_base_url, id, 
        )
        kwargs["vs_currency"] = vs_currency
        kwargs["days"] = days

        return self.__request(api_url, kwargs)
