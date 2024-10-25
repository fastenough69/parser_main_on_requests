from string import digits
from time import time, sleep
import asyncio
import aiohttp
from os import getenv

def get_time(func):
    async def wrapper(*args, **kwargs):
        try:
            timer = time()
            result = await func(*args, **kwargs)
            print(f'Time execute: {time() - timer:.2f} seconds\nPress "F5" no Desktop to display the file')
            return result
        except Exception as e:
            print(f'There been an error: {e}')
            print(f'Time execute: {time() - timer:.2f} seconds\nPress "F5" no Desktop to display the file')
            return
        finally:
            input('Press Enter to close the programme...')
    return wrapper

async def response_mail(sesion, mail_name: str, name_url: str):
    url = 'https://api.products.aspose.app/email/api/Checker/Check'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'api.products.aspose.app',
        'Origin': 'https://products.aspose.app',
        'Referer': 'https://products.aspose.app/',
        'Sec-Ch-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'Sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
    }
    data = {
    'email': mail_name
    }
    async with sesion.post(url, headers=headers, data=data) as response:
        data = await response.json()
        if data['existenceStatus'] == 'Exists':
            return data['email'], name_url
        else:
            return 0, 0

def check_name_mail(data: list):
    return [name for name in data if '_' not in name[1] or ' ' not in name[1] or name[1][0] not in digits]

@get_time
async def main():
    name_file = input('Input full path file with emails: ')
    user = getenv('USERNAME') 
    with open(name_file, 'r') as input_file:
        temp = input_file.readlines()
    async with aiohttp.ClientSession() as session:
        data = [line.strip().split('|') for line in temp if line != '\n']
        data = check_name_mail(data)
        tasks_gmail = [response_mail(session, name[1] + '@gmail.com', name[0]) for name in data]
        tasks_inbox = [response_mail(session, name[1] + '@inbox.me', name[0]) for name in data]
        tasks_icloud =  [response_mail(session, name[1] + '@icloud.com', name[0]) for name in data]
        tasks = tasks_inbox + tasks_gmail + tasks_icloud
        res = await asyncio.gather(*tasks)
        with open(f'C:\\Users\\{user}\\Desktop\\output.txt', 'w') as output_file:
            for mail, mail_url in res:
                if mail and mail_url: output_file.writelines(f'{mail}\t{mail_url}\n')

if __name__ == '__main__':
    asyncio.run(main())
