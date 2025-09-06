import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor
import time

chars = string.digits

words = []
LOWEST = 1557950
HIGHEST = 1563952

with open("words.txt", "r") as file:
    for line in file.read().splitlines():
        words.append(line[:8])

MESSAGE = "message here :p"
COOKIES = {

}
USERKEY = "userkey here :p"
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://0.newgrounds.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://0.newgrounds.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def send_comment(i: str):
    if i:
        data = {
            'body': f'{MESSAGE} || {" ".join(random.choices(words, k=6))}',
            'userkey': USERKEY,
            'isAjaxRequest': '1',
        }
        print(data["body"])
        response = requests.post(i, cookies=COOKIES, headers=HEADERS, data=data, timeout=10)
        try:
            print(response.url)
            print(response.json())
        except Exception as e:
            print(response.status_code)

r = range(10)

def get_post(id):
    try:
        response = requests.get(f'https://0.newgrounds.com/news/post/{id}', cookies=COOKIES, headers=HEADERS,timeout=10)
        if response.status_code == 200:
            url = response.json()['url']
            return f"https://{url.split('://')[1].split('.')[0]}.newgrounds.com/news/comments/{url.split('/')[-1]}/comment"
        return None
    except:
        return None

while True:
    ids = []
    with ThreadPoolExecutor(max_workers=15) as ex:
        futures = []
        for i in r:
            futures.append(ex.submit(get_post, random.randint(LOWEST,HIGHEST)))
        for future in futures:
            ids.append(future.result())
    print(ids)
    ids = filter(None, ids)
    time.sleep(2)
    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(send_comment, ids)

    time.sleep(60)
