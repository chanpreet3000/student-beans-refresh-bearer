import os
import requests

from random import shuffle
from typing import Dict, List
from Logger import Logger
from dotenv import load_dotenv

load_dotenv()


class ProxyManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProxyManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.proxies: List[Dict[str, str]] = self.__fetch_proxies()
        self.current_index: int = 0
        self._initialized = True
        Logger.info("ProxyManager initialized")

    @classmethod
    def __fetch_proxies(cls) -> List[Dict[str, str]]:
        """Fetch proxies from Webshare API"""
        Logger.info("Fetching new proxies from Webshare")
        webshare_api_token = os.getenv('webshare_api_token')

        response = requests.get(
            f"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=250",
            headers={"Authorization": f"Token {webshare_api_token}"},
            timeout=10
        )
        response.raise_for_status()
        proxies_list = response.json().get('results', [])

        formatted_proxies = []
        for proxy in proxies_list:
            url = f"http://{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}"
            proxy['http'] = url
            proxy['https'] = url
            formatted_proxies.append(proxy)

        shuffle(formatted_proxies)
        Logger.info(f"Successfully loaded {len(formatted_proxies)} proxies")
        return formatted_proxies

    def get_proxy(self) -> Dict[str, str]:
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        Logger.debug("Providing proxy", proxy)
        return proxy
