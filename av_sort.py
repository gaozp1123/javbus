import re
import requests
import os
from bs4 import BeautifulSoup
import shutil
dirroot = 'E:\视频\\unkonw'
# 本地代理设置
proxy = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
# 代理头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
av_list = []
av_exten = []
av = []
for root, dirs, files in os.walk(
        dirroot, topdown=False):
    for fullname in files:
        av.append(fullname)
        name, exten = os.path.splitext(fullname)
        temp = 'https://www.javbus.com/'+str(name)
        av_list.append(temp)
        av_exten.append(exten)

for i in range(len(av_list)):
    print(av_list[i])
    try:
        response = requests.get(av_list[i],headers=headers,proxies=proxy)
    except ConnectionError as e:
        print(e.args)
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.title.string == "404 Page Not Found!":
        pass
    else:
        actors = re.findall(
            '<a href="https://www.javbus.com/star/.{2,5}">(.{1,8})</a>',
            response.text)
        if len(actors)>0:
            src = os.path.join(root, av[i])
            dstdir = os.path.join('E:\视频\porn',actors[0])
            print(dstdir)
            if not os.path.exists(dstdir):
                os.mkdir(dstdir)
            try:
                shutil.move(src=src, dst=dstdir)
            except shutil.Error as e:
                print("error")
