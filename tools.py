import time
import json
import aiofiles
import requests
from logger import logger
from web3.auto import w3
from eth_account.messages import encode_defunct
from evm_wallet import Wallet


async def timer():
    return int(time.time())


async def get_address(private_key):
    wallet = Wallet(private_key, 'Ethereum')
    return wallet.public_key


async def read_file_lines(filename):
    async with aiofiles.open(filename, 'r') as file:
        lines = await file.readlines()
    return [line.strip() for line in lines]


async def append_file_lines(filename, line):
    async with aiofiles.open(filename, 'a') as file:
        await file.write(line + '\n')


# def signature(message, private_key, timestamp):
#     msg = f'{message}\n\nTimestamp: {timestamp}'
#     msg =  encode_defunct(text=msg)
#     signed_message =  w3.eth.account.sign_message(
#         msg, private_key=private_key)

#     signature = signed_message.signature

#     return signature.hex()[2:]


async def signature(message, private_key, timestamp):
    msg = f'{message}\n\nTimestamp: {timestamp}'
    encoded_message = encode_defunct(text=msg)
    signed_message = w3.eth.account.sign_message(
        encoded_message, private_key=private_key)

    signature = signed_message.signature

    return signature.hex()[2:]


# def update_info(id, address, accounts, filename, message):
#     with open(filename, 'w') as file:
#         json.dump(accounts, file, indent=4)
#     logger.info(f" {id} | {address} | {message}")
#     return accounts

async def update_info(id, address, accounts, filename, message):
    try:
        async with aiofiles.open(filename, 'w') as file:
            await file.write(json.dumps(accounts, indent=4))
        logger.info(f" {id} | {address} | {message}")
        return accounts
    except Exception as e:
        logger.error(f"Update information failed: {e}")
        return None

# def get_accounts(filename):
#     try:
#         with open(filename, 'r') as file:
#             accounts = json.load(file)
#             return accounts
#     except FileNotFoundError:
#         return {}


async def get_accounts(filename):
    try:
        async with aiofiles.open(filename, 'r') as file:
            content = await file.read()
            accounts = json.loads(content)
            return accounts
    except FileNotFoundError:
        return {}
    # except json.JSONDecodeError:
    #     print(f"Ошибка декодирования JSON в файле {filename}")
    #     return {}
