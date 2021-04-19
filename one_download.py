# 使用star_avs_spider脚本中的函数进行一个女优所有作品的av爬取
import star_avs_spider

if __name__ == '__main__':
    name = input("请输入女优的名字:")
    start_url = input("请输入女优的主页:")
    aStarAvList, page_length = star_avs_spider.process_pages(start_url)
    print(f'{name}一共有{page_length}页')
    print(name + "的av有：" + str(len(aStarAvList)) + ' 部')
    for i in range(len(aStarAvList)):
        print(str(i) + '\t', aStarAvList[i])
        star_avs_spider.process_av(name, aStarAvList[i])