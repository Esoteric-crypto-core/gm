import aiohttp
import time
import random
import asyncio
from tools import *
from logger import logger
from config import *
from fake_useragent import UserAgent
from website import GMRest
from better_proxy import Proxy


class GM(GMRest):
    def __init__(self, id: int, address: str, private_key: str, invite_code: str, proxy: str = None):
        self.proxy = Proxy.from_str(proxy).as_url if proxy else None
        super(GM, self).__init__(id=id, address=address, private_key=private_key,
                                 proxy=self.proxy, invite_code=invite_code)

    async def prepair_tasks(self, launchpad_quests):
        actual_tasks = []

        for quest in launchpad_quests:
            if quest['id'] in TASKS_ID:
                if quest['user_done_status'] == False:
                    actual_tasks.append(quest)

        return actual_tasks

    async def account_tasks_process(self):
        tasks_info = await self.get_tasks()
        await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))

        if int(time.time()) - tasks_info['result']['check_in_task_info']['last_check_in_time'] >= 86760:
            response_json = await self.task(task_id=DAILY_TASK, category=2, message='Daily')
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))

        launchpad_quests = tasks_info['result']['launchpad_tasks_info']

        actual_tasks = await self.prepair_tasks(launchpad_quests)

        if len(actual_tasks) >= 1:
            for _ in range(len(actual_tasks)):
                task = random.choice(actual_tasks)
                actual_tasks.remove(task)
                # task = actual_tasks.pop(
                #     random.choice(range(len(actual_tasks))))
                task_id = task['id']
                message = task['title']

                if task_id != "910388748538945778":
                    task_response = await self.task(task_id=task_id, category=1, message=f'{message} Send request')
                    await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))
    
                    if task_response['success'] == True:
                        await self.task(task_id=task_id, category=2, message=message)
                        await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))
                task_response = await self.task(task_id=task_id, category=2, message=f'{message} claimed')

            logger.info(f" {self.id} | {self.address} | Tasks completed!")

    async def login_process(self):
        response = await self.response()
        await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))
        new_accounts = await read_file_lines("data/new_accounts.txt")
        accounts = await get_accounts('data/accounts.json')

        response_json = await self.login()

        if self.address not in new_accounts:
            await append_file_lines("data/new_accounts.txt", self.address)

        if response_json["result"]["user_info"]["agent"] == {}:
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))

            response_invite = await self.inviting()
            accounts[self.address]["self_invite_code"] = response_invite['result']['user_info']['invite_code']
            await append_file_lines(filename='data/new_codes.txt', line=response_invite['result']['user_info']['invite_code'])
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))

            response_agent = await self.agent_set()
            accounts[self.address]['nft_id'] = response_agent['result']['nft_id']
            accounts[self.address]['rarity'] = response_agent['result']['rarity']
            accounts[self.address]['image'] = response_agent['result']['image']

            await update_info(self.id, self.address, accounts,
                              filename='data/accounts.json', message="Account info update")
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))

        else:
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))

    async def account_process(self):
        try:
            await asyncio.sleep(random.randint(MIN_TIME_ACCOUNT, MAX_TIME_ACCOUNT))

            await self.login_process()
            await self.account_tasks_process()
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))
            await self.get_energy()
            await asyncio.sleep(random.randint(MIN_TIME, MAX_TIME))
            await self.get_account_info()
        finally:
            await self.close_session()
