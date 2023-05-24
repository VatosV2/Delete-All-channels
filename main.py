import asyncio
import aiohttp
from colorama import Fore, Style
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


class Log:
    @staticmethod
    def err(msg):
        print(f'{Style.BRIGHT}[{Fore.LIGHTRED_EX} ERROR {Fore.RESET}]: {msg}')

    @staticmethod
    def succ(msg):
        print(f'{Style.BRIGHT}[{Fore.LIGHTGREEN_EX} SUCCESS {Fore.RESET}]: {msg}')

    @staticmethod
    def console(msg):
        print(f'{Style.BRIGHT}[{Fore.LIGHTBLUE_EX} CONSOLE {Fore.RESET}]: {msg}')

    @staticmethod
    def invalid(msg):
        print(f'{Style.BRIGHT}[{Fore.LIGHTMAGENTA_EX} INVALID {Fore.RESET}]: {msg}')


lc = (Fore.RESET + "[" + Fore.LIGHTMAGENTA_EX + ">" + Fore.RESET + "]")

clear()
Log.console("If you use too often, your API limit gets affected.")
bot_token = input(lc + "Enter Bot Token: ")
guild_id = input(lc + "Enter guild ID: ")

headers = {
    'Authorization': f'Bot {bot_token}',
    'Content-Type': 'application/json'
}

async def delete_channel(session, channel_id):
    url = f'https://discord.com/api/v9/channels/{channel_id}'
    async with session.delete(url) as response:
        if response.status == 204 or response.status == 200:
            Log.succ(f'Deleted channel {channel_id}')
        else:
            Log.err(f'Failed to delete channel {channel_id}. Status code: {response.status}')

async def delete_channels():
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
            async with session.get(url) as response:
                if response.status == 200:
                    channels = await response.json()
                    if len(channels) == 0:
                        Log.succ("all channels were deleted.")
                        input("")
                        break
                    deletion_tasks = []
                    for channel in channels:
                        deletion_tasks.append(delete_channel(session, channel['id']))
                    await asyncio.gather(*deletion_tasks)
                else:
                    print(f'Failed to fetch channels. Status code: {response.status}')
                    break

    
loop = asyncio.get_event_loop()
loop.run_until_complete(delete_channels())
