from selenium import webdriver
import time
from lxml import etree
import re
import json
from urllib.request import urlopen
from urllib.request import Request
# from urllib.error import


if __name__ == "__main__":
    urls = []
    imgUrls = []
    #TODO Store baseurl in file
    baseUrl = 'https://www.bing.com'
    with open("./url.txt") as furl:
        urls.append(furl.readline())
    furl.close()

    #TODO add phantomjs config file
    # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors = true',
    #                                            '--load-image=true', # usually this is false
    #                                            '--disk-cache=false'])
    # driver = webdriver.PhantomJS()

    for url in urls:
        #TODO AUTO set idx & n
        #now day - lastest day = {n}
        #{idx}=0
        idx = 14 # 0->2->4->cur
        n = 10  # 2->2->10->cur but only get 3 new img => guess only 15 img is available #TODO idx & n has limitation
        url = url.replace('{idx}',str(idx)).replace('{n}',str(n))
        # driver.get(url)
        # driver.set_window_size(height=4000)
        # time.sleep(2)
        # content = driver.page_source
        request = Request(url)
        response =urlopen(request)
        content = response.read().decode('utf-8')

        #parse content by xpath
        # tree = etree.HTML(content)
        # imgContainer = tree.xpath(u"//*[@id='bgDiv']")[0]
        # tmp = tree.xpath(u"//*[@id='bgDiv']")[0].attrib['style']
        #'width: 1115px; height: 628px; top: -14.5px;
        # left: 0px;
        # background-image: url(https://www.bing.com/az/hprichbg/rb/Rapadalen_ZH-CN11779950174_1920x1080.jpg);
        # opacity: 1;'
        # imgUrl = re.findall('url\(([^)]*)', tmp)
        # imgUrls.append(imgUrl)

        # parse content with json
        res = json.loads(content)
        images = res['images']
        for image in images:
            imgUrls.append(image['url']+";"+image['startdate'])

    ##driver.close()
    # driver.quit()
    for imgUrl in imgUrls:
        dateinfo = imgUrl.split(';')[-1]
        tmpUrl = imgUrl.split(';')[0]
        fileType = tmpUrl.split('.')[-1]
        fileName = './img/'+dateinfo+'.'+fileType

        curUrl = baseUrl + tmpUrl
        response = urlopen(curUrl)

        with open(fileName,'wb') as fimg:
            fimg.write(response.read())
        fimg.close()

#TODO cmd set window background
