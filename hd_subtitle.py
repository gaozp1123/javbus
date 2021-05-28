# 此脚本获取www.javbus.com中一个女优的带字幕的电影的种子连接
import lxml.html
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
# 本地代理设置
proxy = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
# 代理头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


def get_download_link(durl):
    r = ''
    try:
        r = requests.get(url=durl, headers=headers, proxies=proxy)
    except BaseException as e:
        print(e)
    avinfo = r.text
    gid = re.search(r'var gid = (\d{10,12});', avinfo).group(1)
    uc = re.search(r'var uc = (\d+);', avinfo).group(1)
    img = re.search('var img = \'(.*)\';', avinfo).group(1)

    ajaxheaders = {
        'referer': 'url',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'x-requested-with': 'XLHttpRequest'
    }
    requesturl = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=' + gid + '&lang=zh&img=' + \
                 img + '&uc=' + uc + '&floor=' + str(46)
    try:
        ajaxresponse = requests.get(
            url=requesturl,
            headers=ajaxheaders,
            proxies=proxy)
        return ajaxresponse.text
    except BaseException as e:
        print(e)


def get_movies(homepage):
    # 获取所有的av电影
    count = 2
    response = requests.get(url=homepage, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.text, 'lxml')
    movies = soup.find_all(name='a', attrs={"class": "movie-box"})
    while True:
        url = homepage + '/' + str(count)
        try:
            r = requests.get(url=url, headers=headers, proxies=proxy)
            if r.status_code == 404:
                return movies
            else:
                tempsoup = BeautifulSoup(r.text, 'lxml')
                temp = tempsoup.find_all(
                    name='a', attrs={
                        "class": "movie-box"})
                movies.extend(temp)
        except BaseException as e:
            print(e)
        count += 1


def get_urls(lmovies):
    urlss = []
    for i in range(len(lmovies)):
        if lmovies[i].find(name='button', attrs={
                "class": "btn btn-xs btn-warning"}):
            url = lmovies[i]['href']
            urlss.append(url)
    return urlss


def analy_download_link(download_link):
    tree = etree.HTML(download_link)
    hd_subtitles = tree.xpath(
        '//td[./a[@title="包含字幕的磁力連結"] and ./a[@title="包含高清HD的磁力連結"]]')
    if len(hd_subtitles):
        print(hd_subtitles[0].xpath('./child::*[1]/@href')[0])

    else:
        subtitle = tree.xpath('//td[./a[@title="包含字幕的磁力連結"]]')[0]
        print(subtitle.xpath('./child::*[1]/@href')[0])


if __name__ == '__main__':
    index = input("请输入主页 ")
    movies = get_movies(index)
    print(f"一共有{len(movies)}部电影，其中", end='')
    subtitle_urls = get_urls(movies)
    print(f"一共有{len(subtitle_urls)}部字母电影")
    for url in subtitle_urls:
        download_links = get_download_link(url)
        analy_download_link(download_links)
