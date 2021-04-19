# 爬取所有女优的信息
import requests
from star_avs_spider import store_av
import re
from retrying import retry

all_star = []

with open("star.txt", encoding='utf-8') as f:
    for item in f.readlines():
        if item != '\n':
            all_star.append(item)

    f.close()
# 保存csv的标题头
csv_headers = [
    '女优',
    '主页',
    '年龄',
    '身高',
    '生日',
    '胸圍',
    '腰圍',
    '臀圍',
    '磁力影片数量',
    '所有影片数量',
]
# 本地代理设置
proxy = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
# 代理头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


@retry(stop_max_attempt_number=700)
def request_star_info(url):
    print(url)
    try:
        response = requests.get(url=url, proxies=proxy)
        if response.status_code == 404:
            return False
        else:
            get_back = response
            return get_back
    except ConnectionError as e:
        print("连接出错误，重新开始")
        raise e


def process_info(data):
    star_info = {}
    star_info['主页'] = data.url
    temp_age = re.findall(r'年齡: (\d\d)', data.text)
    title = re.findall('<title>(.+)</title>', data.text)[0]
    actor = title.split('-')[0]
    star_info['女优'] = actor
    if len(temp_age) != 0:
        age = temp_age[0]
        star_info['年齡'] = age
    else:
        star_info['年齡'] = ''
    temp_height = re.findall(r'身高: (\d{3})cm', data.text)
    if len(temp_height) != 0:
        height = temp_height[0]
        star_info['身高'] = height
    else:
        star_info['身高'] = ''
    temp_birthday = re.findall(r'生日: (\d{4}-\d{2}-\d{2})', data.text)
    if len(temp_birthday) != 0:
        birthday = temp_birthday[0]
        star_info['生日'] = birthday
    else:
        star_info['生日'] = ''
    temp_Cupsize = re.findall(r'罩杯: (\d)', data.text)
    if len(temp_Cupsize) != 0:
        Cupsize = temp_Cupsize[0]
        star_info['罩杯'] = Cupsize
    else:
        star_info['罩杯'] = ''
    temp_Chestgirth = re.findall(r'胸圍: (\d{2})cm', data.text)
    if len(temp_Chestgirth) != 0:
        Chestgirth = temp_Chestgirth[0]
        star_info['胸圍'] = Chestgirth
    else:
        star_info['胸圍'] = ''
    temp_Waistcircumference = re.findall('腰圍: (.{1,4})cm', data.text)
    if len(temp_Waistcircumference) != 0:
        Waistcircumference = temp_Waistcircumference[0]
        star_info['腰圍'] = Waistcircumference
    else:
        star_info['腰圍'] = ''
    temp_Buttocks = re.findall('臀圍: (.{1,4})cm', data.text)
    if len(temp_Buttocks) != 0:
        Buttocks = temp_Buttocks[0]
        star_info['臀圍'] = Buttocks
    else:
        star_info['臀圍'] = ''
    resource_movie = re.findall('&nbsp;已有磁力&nbsp;(.{1,4})&nbsp;', data.text)[0]
    star_info['磁力影片数量'] = resource_movie
    all_movie = re.findall('&nbsp;全部影片&nbsp;(.{1,4})&nbsp;', data.text)[0]
    star_info['所有影片数量'] = all_movie
    return star_info


if __name__ == '__main__':
    for i in range(38392, len(all_star)):
        print(f"第{i}个", end='\t')
        data = request_star_info(all_star[i].rstrip())
        if data is False:
           pass
        else:
            a_actor_info = process_info(data)
            print(a_actor_info)
            csvdata = [
                a_actor_info['女优'],
                a_actor_info['主页'],
                a_actor_info['年齡'],
                a_actor_info['身高'],
                a_actor_info['生日'],
                a_actor_info['胸圍'],
                a_actor_info['腰圍'],
                a_actor_info['臀圍'],
                a_actor_info['磁力影片数量'],
                a_actor_info['所有影片数量'], ]
            store_av('all_star.csv', csv_headers, csvdata)
