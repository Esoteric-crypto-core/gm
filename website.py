import json
import random
import aiohttp
import asyncio
from session import BaseClient
from logger import logger
from config import *
from tools import *
from tenacity import retry, stop_after_attempt, wait_random, retry_if_not_exception_type


class GMRest(BaseClient):
    def __init__(self, id: int, address: str, private_key: str, invite_code: str, proxy: str = None):
        super().__init__(proxy)
        self.address = address
        self.private_key = private_key
        self.invite_code = invite_code

        self.id = id
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(trust_env=True,
                                                                    connector=aiohttp.TCPConnector(ssl=False))

    async def response(self):
        response = await self.session.get(
            url=f"https://launchpad.gmnetwork.ai/mission?invite_code={
                self.invite_code}", headers=self.website_headers, proxy=self.proxy)
        if response.status != 200:
            raise aiohttp.ClientConnectionError(f" {self.id} | Response: | {await response.text()}")

    @retry(stop=stop_after_attempt(7),
           before_sleep=lambda retry_state, **kwargs: logger.info(
               f"{retry_state.outcome.exception()} | Create Account Retrying... "),
           reraise=True)
    async def login(self):
        try:
            logger.info(f' {self.id} | {self.address} | Login starts...')
            solution = await self.captcha_process()
            headers = self.website_headers.copy()
            headers["cf-turnstile-resp"] = solution

            url = 'https://api-launchpad.gmnetwork.ai/user/login/'
            message = 'Welcome to GM Launchpad.\nPlease sign this message to login GM Launchpad.'
            timestamp = await timer()
            sign = await signature(message=message, private_key=self.private_key, timestamp=timestamp)

            data = {
                'address': self.address,
                'message': message,
                'timestamp': timestamp,
                'signature': sign,
                'login_type': 100,
            }
            data_json = json.dumps(data)

            response = await self.session.post(url, headers=headers, data=data_json,
                                               proxy=self.proxy)

            if response.status != 200 or "error" in await response.text():
                raise aiohttp.ClientConnectionError(f" {self.id} | Create acc response: | {await response.text()}")
            response_json = await response.json()
            self.access_token = response_json["result"]['access_token']
            await self.add_access_token()

            if response_json["result"]["user_info"]["agent"] == {}:
                logger.info(f" {self.id} | {
                            self.address} | New account created!")
                return response_json

            logger.info(f" {self.id} | {self.address} | Account login")

            return response_json

        except aiohttp.ClientConnectionError as e:
            logger.error(
                f" {self.id} | Client connection error for account: {e}")
            raise e
        except Exception as e:
            logger.error(
                f" {self.id} | Unexpected error during login for account: {e}")
            raise e

    async def add_access_token(self):
        self.website_headers['access-token'] = self.access_token

    async def inviting(self):
        url = 'https://api-launchpad.gmnetwork.ai/user/invite_code/'

        data = {
            'invite_code': self.invite_code,
            'address': self.address,
        }
        data_json = json.dumps(data)

        response = await self.session.post(url, headers=self.website_headers, data=data_json,
                                           proxy=self.proxy)

        if response.status != 200 or "error" in await response.text():
            raise aiohttp.ClientConnectionError(f" {self.id} | Invite acc response: | {await response.text()}")
        logger.info(f" {self.id} | {self.address} | Account invited!")

        return await response.json()

    async def agent_set(self):
        url = 'https://api-launchpad.gmnetwork.ai/user/auth/agent_set/'

        data = {
            'nft_id': '',
        }

        data_json = json.dumps(data)
        response = await self.session.post(url, headers=self.website_headers, data=data_json,
                                           proxy=self.proxy)

        if response.status != 200 or "error" in await response.text():
            raise aiohttp.ClientConnectionError(f" {self.id} | Agent set response: | {await response.text()}")
        logger.info(f" {self.id} | {self.address} | Agent set!")

        return await response.json()

    async def get_tasks(self):
        url = 'https://api-launchpad.gmnetwork.ai/task/auth/task_center/'

        params = {
            'season_um': '1',
        }

        response = await self.session.get(url, headers=self.website_headers, params=params,
                                          proxy=self.proxy)
        if response.status != 200 or "error" in await response.text():
            raise aiohttp.ClientConnectionError(f" {self.id} | Tasks getting failed | {await response.text()}")
        logger.info(f" {self.id} | Tasks info get successfuly")

        return await response.json()

    async def tasks_status(self, task_id):
        response = await self.get_tasks()

        if response["result"]["check_in_task_info"]["id"] == task_id:
            return response["result"]["check_in_task_info"]["user_check_in_count"]

        for i in response["result"]["questn_tasks_info"]:
            if i["id"] == task_id:
                return i["user_done_status"]

    async def task(self, task_id, category, message):
        url = 'https://api-launchpad.gmnetwork.ai/task/auth/task/'

        data = {
            'task_id': task_id,
            'category': category*100,
        }

        data_json = json.dumps(data)
        response = await self.session.post(url, headers=self.website_headers, data=data_json,
                                           proxy=self.proxy)
        response_json = await response.json()

        if response.status != 200 or "error" in await response.text():
            raise aiohttp.ClientConnectionError(f" {self.id} | {message} task response: | {await response.text()}")
        if response_json['success'] == True:
            logger.info(f" {self.id} | {self.address} | {
                message} task complete!")

        return response_json

    async def get_energy(self):
        url = 'https://api-launchpad.gmnetwork.ai/energy/auth/user_energy/'

        response = await self.session.get(url, headers=self.website_headers, proxy=self.proxy)
        response_json = await response.json()

        if response.status != 200 or "error" in await response.text():
            raise aiohttp.ClientConnectionError(f" {self.id} | Get energy failed: | {await response.text()}")

        if isinstance(response_json["result"]["daily"], list):
            daily_energy = response_json["result"]["daily"][0]
        else:
            daily_energy = response_json["result"]["daily"]
        daily_energy = float(str(daily_energy).replace(
            '(', '').replace(')', '').replace(',', '').strip())
        total_energy = float(response_json["result"]["total_energy"])

        logger.info(f" {self.id} | {self.address} | Daily energy: {
                    daily_energy}; Total energy: {total_energy}")

        await self.update_energy(daily_energy=daily_energy, total_energy=total_energy)

    async def update_energy(self, daily_energy, total_energy):
        accounts = await get_accounts('data/accounts.json')

        accounts[self.address]['daily'] = daily_energy
        accounts[self.address]['total'] = total_energy

        await update_info(id=self.id, address=self.address, accounts=accounts, filename='data/accounts.json', message='Energy info updated')

    async def get_account_info(self):
        accounts = await get_accounts('data/accounts.json')
        url = 'https://api-launchpad.gmnetwork.ai/user/auth/info/'
        response = await self.session.get(url, headers=self.website_headers, proxy=self.proxy)
        response_json = await response.json()

        if response.status != 200 or "error" in await response.text():
            raise aiohttp.ClientConnectionError(f" {self.id} | Get account info failed: | {await response.text()}")

        account_level = int(response_json["result"]["level"])
        if account_level > accounts[self.address]['level']:
            accounts[self.address]['level'] = account_level

        if accounts[self.address]["self_invite_code"] == "":
            accounts[self.address]["self_invite_code"] = response_json["result"]["invite_code"]
        if accounts[self.address]["nft_id"] == 0:
            accounts[self.address]["nft_id"] = response_json["result"]["agent"]["nft_id"]
        if accounts[self.address]["rarity"] == 0:
            accounts[self.address]["rarity"] = response_json["result"]["agent"]["rarity"]
        if accounts[self.address]["image"] == "":
            accounts[self.address]["image"] = response_json["result"]["agent"]["image"]

        await update_info(id=self.id, address=self.address, accounts=accounts, filename='data/accounts.json', message='Account info updated')

    async def send_captcha_request(self, api_key, site_key, page_url):
        if CAPTCHA_SERVICE != '2captcha':
            url = CAPTCHA_SERVICES[CAPTCHA_SERVICE]['createTask']
            data = {
                "clientKey": api_key,
                "task": {
                    "type": "TurnstileTaskProxyless",
                    "websiteURL": page_url,
                    "websiteKey": site_key
                }
            }

            if self.proxy:
                data['task']['type'] = 'TurnstileTask'
                data['task']['proxyType'] = 'http'
                data['task']['proxyAddress'] = self.proxy.split(
                    '@')[1].split(':')[0]
                data['task']['proxyPort'] = self.proxy.split(
                    '@')[1].split(':')[1]
                data['task']['proxyLogin'] = self.proxy.split(
                    '@')[0].split('//')[1].split(':')[0]
                data['task']['proxyPassword'] = self.proxy.split(
                    '@')[0].split(':')[-1]
                data['task']['userAgent'] = self.website_headers['user-agent']

            response = await self.session.post(url, json=data)
            result = await response.json()
            if result['errorId'] == 0:
                return result['taskId']
            else:
                raise Exception(
                    f" {self.id} | Failed to send captcha request: " + result['errorDescription'])

        if CAPTCHA_SERVICE == '2captcha':
            url = CAPTCHA_SERVICES[CAPTCHA_SERVICE]['createTask']
            params = {
                "key": api_key,
                "method": "turnstile",
                "sitekey": site_key,
                "pageurl": page_url
            }

            if self.proxy:
                proxy_parts = self.proxy.split('@')
                auth = proxy_parts[0].split('//')[1].split(':')
                address = proxy_parts[1].split(':')
                params.update({
                    "proxy": f"{auth[0]}:{auth[1]}@{address[0]}:{address[1]}",
                    "proxytype": "HTTP"
                })

            response = await self.session.get(url, params=params)
            text = await response.text()
            if "OK|" in text:
                captcha_id = text.split("|")[1]
                return captcha_id
            else:
                raise Exception(
                    f" {self.id} | Failed to send captcha request: {text}")

    async def get_captcha_solution(self, api_key, task_id):
        if CAPTCHA_SERVICE != '2captcha':
            url = CAPTCHA_SERVICES[CAPTCHA_SERVICE]['getTask']
            data = {
                "clientKey": api_key,
                "taskId": task_id
            }

            while True:
                response = await self.session.post(url, json=data)
                result = await response.json()
                if result['errorId'] == 0:
                    if result['status'] == 'ready':
                        return result['solution']['token']
                    else:
                        await asyncio.sleep(5)
                else:
                    raise Exception(
                        f" {self.id} | Failed to get captcha solution: " + result['errorDescription'])

        if CAPTCHA_SERVICE == '2captcha':
            url = CAPTCHA_SERVICES[CAPTCHA_SERVICE]['getTask']
            params = {
                "key": api_key,
                "action": "get",
                "id": task_id
            }

            while True:
                response = await self.session.get(url, params=params)
                text = await response.text()
                if "OK|" in text:
                    captcha_result = text.split("|")[1]
                    return captcha_result
                elif "CAPCHA_NOT_READY" in text:
                    await asyncio.sleep(5)
                else:
                    raise Exception(
                        f" {self.id} | Failed to get captcha solution: {text}")

    async def captcha_process(self):
        task_id = await self.send_captcha_request(api_key=API_KEY, site_key=SITE_KEY, page_url=PAGE_URL+self.invite_code)
        logger.info(f' {self.id} | {
                    self.address} | Getting captcha solution...')
        await asyncio.sleep(40)
        solution = await self.get_captcha_solution(api_key=API_KEY, task_id=task_id)
        return solution

    async def close_session(self):
        await self.session.close()
