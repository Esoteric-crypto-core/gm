from curl_cffi import requests
from user_agent import *


class BaseClient:

    def __init__(self, proxy: str = None):
        self.session = None
        self.ip = None
        self.username = None
        self.proxy = None
        self.access_token = None

        # self.user_agent = user_agent
        self.proxy = proxy

        chrome_version_details, windows_nt_version, arch, bitness = get_random()
        self.website_headers = {
            'authority': 'api-launchpad.gmnetwork.ai',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://launchpad.gmnetwork.ai',
            'referer': 'https://launchpad.gmnetwork.ai/',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            "accept": "*/*",
            "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": f"Mozilla/5.0 (Windows NT {windows_nt_version}; Win64; {arch}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version_details['full_version']} Safari/537.36",
            "sec-ch-ua": f'"Google Chrome";v="{chrome_version_details["major_version"]}", "Not:A Brand";v="99", "Chromium";v="{chrome_version_details["major_version"]}"',
            "sec-ch-ua-arch": f'"{arch}"',
            "sec-ch-ua-bitness": f'"{bitness}"',
            "sec-ch-ua-full-version": f'"{chrome_version_details["full_version"]}"',
            "sec-ch-ua-full-version-list": f'"Google Chrome";v="{chrome_version_details["full_version"]}", "Not:A Brand";v="99", "Chromium";v="{chrome_version_details["full_version"]}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": f'"{windows_nt_version}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "connection": "keep-alive",
        }
        if chrome_version_details == '119':
            self.impersonate = requests.BrowserType.chrome119
        else:
            self.impersonate = requests.BrowserType.chrome120

        #     {
        #     'authority': 'api-launchpad.gmnetwork.ai',
        #     'accept': 'application/json, text/plain, */*',
        #     'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
        #     'content-type': 'application/json',
        #     'origin': 'https://launchpad.gmnetwork.ai',
        #     'referer': 'https://launchpad.gmnetwork.ai/',
        #     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'empty',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-site': 'same-site',
        #     'user-agent': self.user_agent,
        # }
