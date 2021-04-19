# 这个脚本用来爬取www.javbus.com的女优作品
# 将作品信息保存为一个csv文件
import requests
from bs4 import BeautifulSoup
import re
import csv
import os

# 要爬取的女优，格式是python字典
followers = {
    '翔田千里': 'https://www.javbus.com/star/173',
    '葉月美音': 'https://www.javbus.com/star/np8',
    '三上悠亜': 'https://www.javbus.com/star/okq',
    'Hitomi（田中瞳）': 'https://www.javbus.com/star/304',
    '中山香苗': 'https://www.javbus.com/star/pfj',
    '織田真子': 'https://www.javbus.com/star/6xe',
    '牧村彩香': 'https://www.javbus.com/star/sej',
    '若月みいな': 'https://www.javbus.com/star/sod',
    '羽生ありさ': 'https://www.javbus.com/star/q68',
    'KAORI': 'https://www.javbus.com/star/b9f',
    '春菜はな': 'https://www.javbus.com/star/6ya',
    '風間ゆみ': 'https://www.javbus.com/star/2t',
    '白鳥寿美礼': 'https://www.javbus.com/star/7q2',
    'RION': 'https://www.javbus.com/star/p4o',
    '篠田ゆう': 'https://www.javbus.com/star/2pv',
    '吉沢明歩': 'https://www.javbus.com/star/2eg',
    '宝生リリー': 'https://www.javbus.com/star/rqb',
    '優月まりな': 'https://www.javbus.com/star/qzy',
    '澁谷果歩': 'https://www.javbus.com/star/nqz',
    '三浦恵理子': 'https://www.javbus.com/star/8ea',
    '若槻みづな': 'https://www.javbus.com/star/p1f',
    '岡江凛': 'https://www.javbus.com/star/vyb',
    '木下凛々子': 'https://www.javbus.com/star/vwq',
    '吉岡奈々子': 'https://www.javbus.com/star/1x0',
    '安齋らら': 'https://www.javbus.com/star/vkq',
    '後藤里香': 'https://www.javbus.com/star/qxw'
}
# 保存csv的标题头
csv_headers = [
    '番号',
    '链接',
    '标题',
    '发行日期',
    '长度',
    '导演',
    '制作商',
    '发行商',
    '系列',
    '类别',
    '演员',
    '磁力链接']
# 存储目前爬取女优所有作品的列表
star_av_list = []
# 本地代理设置，此网站需要代理连接，本人使用的是v2ray
proxy = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
# 代理头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
# ajax请求磁力链接base地址
baseurl = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid='


def process_pages(star_url):
    # 1.遍历女优所有页，爬取每个页的所有av
    #   返回女优的av列表和页长
    print('第1页提取完毕')
    get_page_items(star_url)
    page_length = 2
    while True:
        request_url = star_url + '/' + str(page_length)
        try:
            response = requests.get(request_url, proxies=proxy, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            if soup.title.string == "404 Page Not Found!":
                page_length -= 1
                return star_av_list, page_length
            else:
                print(f'第{page_length}页提取完毕')
                get_page_items(request_url)
                page_length += 1
        except ConnectionError as e:
            print(e.args)


def get_page_items(page_url):
    # 2.获取当前爬取女友一页有多少av
    try:
        response = requests.get(url=page_url, headers=headers, proxies=proxy)
        if response.status_code == 200:
            items_url = re.findall(
                '<a class="movie-box" href="(.*)">',
                response.text)
            for item in items_url:
                star_av_list.append(item)
            print(f"一共有{len(star_av_list)}个电影了")
    except ConnectionError as e:
        print(e.args)


def process_av(star_name, url):
    #  3.分析一个av的信息
    try:
        response = requests.get(url, proxies=proxy)
    except ConnectionError as e:
        print(e.args)
    av_info = get_av_info(url, response)
    av_info['av_link'] = url
    store_file = star_name + '.csv'
    csvdata = [
        av_info['avid'],
        av_info['av_link'],
        av_info['avdesc'],
        av_info['product_date'],
        av_info['duartion'],
        av_info['director'],
        av_info['producer'],
        av_info['issuer'],
        av_info['series'],
        av_info['Category'],
        av_info['actors'],
        av_info['download_link']]
    store_av(store_file, csv_headers, csvdata)


def get_av_info(url, response):
    # 4.返回av的信息，python字典
    av_info = {}
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    # 获取到的网页信息需要进行解析，使用lxml解析器，其实默认的解析器就是lxml，但是这里会出现警告提示，方便你对其他平台移植
    webtitle = str(soup.h3.string)
    # print(webtitle)
    av_info['avid'] = webtitle.split(" ")[0]
    # print(avid)
    av_info['avdesc'] = webtitle[len(av_info['avid']) + 1:len(webtitle)]
    av_info['product_date'] = re.search(
        r'\d\d\d\d.\d\d.\d\d', response.text).group(0)
    if re.search(r'(\d+)分鐘', response.text) is not None:
        av_info['duartion'] = re.search(r'(\d+)分鐘', response.text).group(1)
    else:
        av_info['duartion'] = ''

    if re.search('導演:<.*">(.*)</a></p>', response.text) is not None:
        av_info['director'] = re.search(
            '導演:<.*">(.*)</a></p>', response.text)[1]
    else:
        av_info['director'] = ''
    if re.search('系列:<.*">(.*)</a>', response.text) is not None:
        av_info['series'] = re.search('系列:<.*">(.*)</a>', response.text)[1]
    else:
        av_info['series'] = ''
    av_info['Category'] = re.findall(
        '<span class="genre">.*">(.*)</a></span>',
        response.text)
    if re.search('製作商:<.*">(.*)</a>', response.text) is not None:
        av_info['producer'] = re.search('製作商:<.*">(.*)</a>', response.text)[1]
    else:
        av_info['producer'] = ''
    if re.search('發行商:<.*">(.*)</a>', response.text) is not None:
        av_info['issuer'] = re.search('發行商:<.*">(.*)</a>', response.text)[1]
    else:
        av_info['issuer'] = ''
    if re.findall(
            '<a href="https://www.javbus.com/star/.{3,5}">(.{1,8})</a>', response.text) is not None:
        av_info['actors'] = re.findall(
            '<a href="https://www.javbus.com/star/.{3,5}">(.{1,8})</a>',
            response.text)
    else:
        av_info['actors'] = ''
    gid = re.search(r'var gid = (\d{10,12});', response.text).group(1)
    uc = re.search(r'var uc = (\d+);', response.text).group(1)
    img = re.search('var img = \'(.*)\';', response.text).group(1)
    ajaxget = re.findall(
        r'(magnet:\?xt=urn:btih:[0-9a-fA-F]{40}.*[^\',\'_self\')])">',
        get_downloadlink(
            url,
            gid,
            uc,
            img))
    av_info['download_link'] = list(set(ajaxget))
    return av_info


def get_downloadlink(url, gid, uc, img):
    # 5.获取一个av的磁力链接
    # ajax请求头
    ajaxheaders = {
        'referer': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'x-requested-with': 'XLHttpRequest'
    }
    requesturl = baseurl + gid + '&lang=zh&img=' + \
        img + '&uc=' + uc + '&floor=' + str(46)
    try:
        ajaxresponse = requests.get(
            url=requesturl,
            headers=ajaxheaders,
            proxies=proxy)
        if ajaxresponse.status_code == 200:
            return ajaxresponse.text
    except requests.ConnectionError as e:
        print("error", e.args)


def store_av(stroed_file, store_head, data):
    # 6.保存一个av的数据为csv
    if not os.path.isfile(stroed_file):
        is_first_write = 1
    else:
        is_first_write = 0
    with open(stroed_file, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        if is_first_write:
            writer.writerow(store_head)
        writer.writerow(data)
    f.close()


if __name__ == '__main__':
    for name, star_url in followers.items():
        aStarAvList, page_length = process_pages(star_url)
        print(f'{name}一共有{page_length}页')
        print(name + "的av有：" + str(len(aStarAvList)) + ' 部')
        followers_av = {}
        for i in range(len(aStarAvList)):
            print(f"第{i+1}/{len(aStarAvList)}个" + '\t', aStarAvList[i])
            process_av(name, aStarAvList[i])
        followers_av[name] = aStarAvList
        print(followers_av)
        # 清空列表，开始下一个
        star_av_list = []
