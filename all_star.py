# 此脚本获取www.javbus.com中所有女优的主页地址
import requests
from bs4 import BeautifulSoup
import re

stars = []

# 本地代理设置
proxy = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
# 代理头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
baseurl = 'https://www.javbus.com/actresses'


def do_request():
    i = 1
    while True:
        print(f"第{i}页", end='\t')
        next_url = 'https://www.javbus.com/actresses/' + str(i)
        try:
            response = requests.get(next_url, proxies=proxy)
            soup = BeautifulSoup(response.text, 'lxml')
            if soup.title.string == "404 Page Not Found! - JavBus":
                print("done")
                break
            find_all(response.text)
            print(len(stars))
        except ConnectionError as e:
            raise e
        i += 1


def find_all(text):
    param = r'href="https://www.javbus.com/star/(\w+)'
    temp_star = re.findall(param, text)
    for i in range(len(temp_star)):
        temp_url = "https://www.javbus.com/star/" + str(temp_star[i])
        stars.append(temp_url)


if __name__ == '__main__':
    do_request()
    with open('star.txt', mode='w') as f:
        for i, item in enumerate(stars):
            f.write(item)
            f.write('\n')
