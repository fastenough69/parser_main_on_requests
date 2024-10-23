from string import digits
from time import time
import requests

def get_time(func):
    def decorator(*args):
        timer = time()
        func(*args)
        print(time() - timer)
    return decorator

def response_mail(mail_name: str):
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
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Проверка на успешный статус ответа
        if response.status_code == 200:
            data = response.json()
            
            # Проверка, что нужные ключи присутствуют в ответе
            if 'email' in data and 'isDisposable' in data:
                return data['email'], data['isDisposable']
            else:
                print("Ошибка: не найдены необходимые данные в ответе.")
                return
        else:
            print(f"Ошибка: получен статус {response.status_code}")
            return
    except requests.exceptions.Timeout:
        print("Запрос превысил время ожидания.")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {e}")

def write_file(tpl: tuple):
    with open('C:\\Users\\lisen\\OneDrive\\Рабочий стол\\output.txt', 'w') as output_file:
        if tpl:
            output_file.writelines(f'{tpl[0]}\t\t\tstatus: {tpl[1]}')
        else:
             output_file.writelines(f'-\t\t\tstatus: -')

def check_name_mail(data: list):
    return [name for name in data if '_' not in name and ' ' not in name and name[0] not in digits]

def threanding_first(data: list):
    for i in range(len(data)):
        temp = response_mail(data[i] + '@gmail.com')
        write_file(temp)

@get_time
def main():
    name_file = input('Введите полный путь до файла: ')
    with open(name_file, 'r') as input_file:
        temp = input_file.readlines()
    data = [line.split('|')[1].strip() for line in temp if line != '\n']
    data = check_name_mail(data)
    threanding_first(data)

if __name__ == '__main__':
    main()

