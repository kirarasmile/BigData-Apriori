from lxml import etree
import time
from selenium import webdriver
import csv
# 读取驱动
chrome_driver =  r"./chromedriver.exe"
driver = webdriver.Chrome(executable_path = chrome_driver)
director = u'宁浩'
# 写CSV文件
file_name = './' + director + '.csv'
base_url = 'https://movie.douban.com/subject_search?search_text=' + director + '&cat=1002&start='
out = open(file_name, 'w', newline = '', encoding = 'utf-8-sig')
csv_write = csv.writer(out, dialect = 'excel')
flags=[]

# 下载指定页面的数据
def download(request_url):
    driver.get(request_url)
    time.sleep(1)
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    html = etree.HTML(html)
    # 设置电影名、导演演员的XPATH
    movie_lists = html.xpath("/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']")
    name_lists = html.xpath("/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='meta abstract_2']")
    # 获取返回的数据个数
    num = len(movie_lists)
    if num > 15: # 第一页会有16条数据
        # 默认第一个不是，去掉第一个
        movie_lists = movie_lists[1:]
        name_lists = name_lists[1:]
    for (movie, name_lists) in zip(movie_lists, name_lists):
        # 会存在数据为空的情况
        if name_lists.text is None:
            continue
        # 显示演员名称
        print(name_lists.text)
        names = name_lists.text.split('/')
        # 判断导演是否为指定的director
        if names[0].strip() == director and movie.text not in flags:
            # 将第一个字段设置为电影名称
            names[0] = movie.text
            flags.append(movie.text)
            csv_write.writerow(names)
    print('OK') # 下载成功
    print(num)
    # 如果一页有14个电影，则翻页
    if num >= 14:
        return True
    else:
        return False
# 开始ID为0，每页增加15
start = 0
while start < 10000:
    request_url = base_url + str(start)
    flag = download(request_url)
    if flag:
         start = start + 15
    else:
        break
out.close()
print('finished')