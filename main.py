import time
import json
import aiofiles
import asyncio
import random
import csv
import os
from typing import List, Dict
from config import *
from logger import logger
from gm import GM
from tools import *
from termcolor import cprint
from eth_account import Account as EthAccount


async def update_csv():
    accounts = await get_accounts('data/accounts.json')

    file_empty = not os.path.exists(
        'data/data.csv') or os.path.getsize('data/data.csv') == 0

    async with aiofiles.open('data/data.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "address", "daily", "total", "level", "self_invite_code", "nft_id", "rarity", "image"
        ])

        await f.write(';'.join(writer.fieldnames) + '\n')

        sorted_accounts = sorted(accounts.values(), key=lambda x: x['id'])

        for account in sorted_accounts:
            row = {field: account.get(field, '')
                   for field in writer.fieldnames}
            await f.write(';'.join(map(str, row.values())) + '\n')


async def account_info(id, address, wallet, proxy, invite_code):

    accounts = await get_accounts('data/accounts.json')

    if address not in accounts:
        accounts[address] = {
            "id": id,
            "address": address,
            "wallet": wallet,
            "proxy": proxy,
            "daily": 0,
            "total": 0,
            "level": 0,
            "invite_code": invite_code,
            "self_invite_code": '',
            "nft_id": 0,
            "rarity": 0,
            "image": '',
        }
        await update_info(id,
                          address, accounts, 'data/accounts.json', 'Account info updated')

        account_info = {}
        account_info[address] = accounts[address]
        return account_info

    if accounts[address]['id'] != id:
        accounts[address]['id'] = id
        await update_info(id,
                          address, accounts, 'data/accounts.json', 'Account id updated')

    if accounts[address]['proxy'] != proxy:
        accounts[address]['proxy'] = proxy
        await update_info(id,
                          address, accounts, 'data/accounts.json', 'Proxy updated')

    # if accounts[address]['wallet'] != wallet:
    #     logger.error(f" {id} | {address} | Invalid private key")
    #     return

    account_info = {}
    account_info[address] = accounts[address]
    return account_info


async def main():
    proxies = await read_file_lines('files/proxies.txt')
    wallets = await read_file_lines('files/wallets.txt')
    invite_codes = await read_file_lines('files/invite_codes.txt')

    addresses = []
    for id, w in enumerate(wallets, start=1):
        try:
            addresses.append(EthAccount().from_key(w).address)
        except Exception as e:
            raise Exception(f' {id} | Wrong private key #{id}: {str(e)}')

    if len(proxies) != len(wallets):
        logger.error('Proxies count does not match wallets count')
        return

    for i in range(len(addresses)):
        await account_info(id=i+1, address=addresses[i], wallet=wallets[i], proxy=proxies[i], invite_code=random.choice(invite_codes))

    logger.info(' Preparing accounts...')
    accounts = await get_accounts('data/accounts.json')
    copy_addresses = addresses.copy()

    tasks = []
    for _ in range(len(copy_addresses)):
        address = random.choice(copy_addresses)
        copy_addresses.remove(address)
        account = accounts[address]

        gm_account = GM(
            id=account['id'], address=account['address'], private_key=account['wallet'], invite_code=account['invite_code'], proxy=f"http://{
                account['proxy']}"
        )

        tasks.append(gm_account.account_process())

    await asyncio.gather(*tasks)

    await update_csv()


if __name__ == "__main__":
    cprint('=================================================', 'white')
    cprint('======= ', 'white', end='')
    cprint('https://t.me/esoteric_crypto_core', 'white', end='')
    cprint(' =======', 'white')
    cprint('=================================================', 'white')
    cprint('        https://t.me/esoteric_crypto_core        ', 'white')
    cprint('=================================================', 'white')
    cprint('======= ', 'white', end='')
    cprint('https://t.me/esoteric_crypto_core', 'white', end='')
    cprint(' =======', 'white')
    cprint('=================================================', 'white')

    asyncio.run(main())
