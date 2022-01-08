from os import write
import requests
import json
import inspect
import os.path
import getpass
import random
import time
from colorama import init, Fore

init(autoreset=True)    # initialise Colorama

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

print(Fore.GREEN + "  ___      _   _            ___     _          _    _                ___                  _              _          ")
print(Fore.GREEN + " | _ ) ___| |_| |_ ___ _ _ / _ \ __| |_ _ __ _| |__(_)__ _ _ __ _  _|   \ _____ __ ___ _ | |___  __ _ __| |___ _ _  ")
print(Fore.GREEN + " | _ \/ -_)  _|  _/ -_) '_| (_) / _` | '_/ _` | '_ \ / _` | '  \ || | |) / _ \ V  V / ' \| / _ \/ _` / _` / -_) '_| ")
print(Fore.GREEN + " |___/\___|\__|\__\___|_|  \___/\__,_|_| \__,_|_.__/_\__,_|_|_|_\_, |___/\___/\_/\_/|_||_|_\___/\__,_\__,_\___|_|   ")
print(Fore.GREEN + "                                                                |__/                                                ")

if os.path.exists(f'{path}/credentials.py'):
    import credentials
    user=credentials.username
    password=credentials.password
else:
    user=input(Fore.MAGENTA + 'Podaj E-Mail: ')
    password=getpass.getpass(prompt=Fore.MAGENTA + 'Podaj hasło: ')

bookid=input(Fore.MAGENTA + 'Podaj ID książki: ')

try:
    rpost = requests.post(url=('https://odrabiamy.pl/api/v2/sessions'), json=({"login": f"{user}", "password": f"{password}"})).content
    token = json.loads(rpost).get('data').get('token')
except:
    print(Fore.RED + 'Niepoprawny e-mail lub hasło. A może nie masz premium?')
    exit()

def download_page(token, page, bookid):
    rget = requests.get(url=f'https://odrabiamy.pl/api/v2/exercises/page/premium/{page}/{bookid}', headers={'user-agent':'new_user_agent-huawei-142','Authorization': f'Bearer {token}'}).content.decode('utf-8')
    lists=json.loads(rget).get('data')

    name=lists[0].get('book').get('name').replace('/','')

    if not os.path.exists(f'{path}/{name}-{bookid}'):
        os.makedirs(f'{path}/{name}-{bookid}')

    for exercise in lists:
        if not os.path.exists(f'{path}/{name}-{bookid}'):
            os.makedirs(f'{path}/{name}-{bookid}')
        number=exercise.get('number')
        file=open(f'{path}/{name}-{bookid}/{page}.html', 'a+', encoding='utf-8')
        file.write(f'<head><meta charset="UTF-8"></head>\n<a style="color:red; font-size:25px;">Zadanie {number}</a><br>\n{exercise.get("solution")}<br>')
        file.close()

rget = requests.get(url=f'https://odrabiamy.pl/api/v1.3/ksiazki/{bookid}').content.decode('utf-8')
if rget == '{"'+f'error":"Couldn\'t find Book with \'id\'={bookid}'+'"}':
    print(Fore.RED + 'Złe ID książki!')
    exit()

pages = json.loads(rget).get('pages')
name = json.loads(rget).get('name').replace('/','')
for page in pages:
    if not os.path.exists(f'{path}/{name}-{bookid}/{page}.html'):
        seconds=random.randint(2, 8)
        download_page(token, page, bookid)
        print(Fore.BLUE + f'Pobrano stronę {page}\nNastępna strona zostanie pobrana za {seconds} sekund')
        time.sleep(seconds)
print(Fore.GREEN + 'Pobrano książkę!')

deinit()
