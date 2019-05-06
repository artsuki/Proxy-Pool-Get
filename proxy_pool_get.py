# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Artsuki

"""

These codes are focused on collection of free proxy ips, and test these ips ,form the ip pool at last for multi-thread web crawler
the ips are strings of 'xxx.xxx.xxx.xxx:0000' putted in list and saved as json

本程序收集各免费代理网站ip，并测试，形成代理ip池，以供多线程爬虫使用
附带测试代理ip池、剔除废ip功能
最后将ip字符串'xxx.xxx.xxx.xxx:0000'，放入列表，保存为json文档

"""

import urllib.request
import urllib.parse
from lxml import etree
import time
from multiprocessing.dummy import Pool as ThreadPool
import json


class ProxyGetter:
    def __init__(self):
        self.url1 = [f'http://www.data5u.com/free/{tag}/index.shtml' for tag in ['gngn']]
        self.url2 = [f'http://www.xicidaili.com/nn/{page}' for page in range(1, 10)]
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.address = []
        self.select = ''

    def context_get(self,url):
        request = urllib.request.Request(url=url,headers=self.headers)
        response = urllib.request.urlopen(request,timeout=10.0).read()
        self.select = etree.HTML(response)
        return 
        
    def data5u_get(self):
        for i in self.url1:
            self.context_get(i)
            target = self.select.xpath("//div[@class='wlist']/ul/li/ul[@class='l2']")
            for j in target:
                ip = j.xpath("./span[not(@style)]/li/text()")
                port = j.xpath("./span[@style]/li[@class]/text()")
                if (len(ip)!=0) & (len(port)!=0):
                    ip = ip[0]
                    port = port[0]
                    self.address.append(f'{ip}:{port}')
                else:
                    continue
            time.sleep(2)
        return
        
    def xici_get(self):
        for i in self.url2:
            self.context_get(i)
            target = self.select.xpath("//table[@id]/tr[@class]")
            for j in target:
                ip = j.xpath("./td")[1].xpath("./text()")
                port = j.xpath("./td")[2].xpath("./text()")
                if (len(ip)!=0) & (len(port)!=0):
                    ip = ip[0]
                    port = port[0]
                    self.address.append(f'{ip}:{port}')
                else:
                    continue
            time.sleep(2)
        return
    
    def address_wash(self):
        with open('E:\MyCodes\MyData\proxy_pool.txt', 'r') as fp:
            if json.load(fp):
                self.address.extend(json.load(fp))
        self.address = list(set(self.address))
        print(f'total IPs get: {len(self.address)}')
		
		

def proxy_get():
    proxy = ProxyGetter()
    proxy.data5u_get()
    print('data5u done')
    proxy.xici_get()
    print('xici done')
    proxy.address_wash()
    return proxy


def proxy_test(ip):
    url = 'http://www.baidu.com'
    handler = urllib.request.ProxyHandler({"http": ip})
    opener = urllib.request.build_opener(handler)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    request = urllib.request.Request(url=url,headers=headers)
    try:
        response = opener.open(request,timeout=10.0)
    except Exception as e:
        print('<Invalid ip>',end=' ')
        return
    else:
        print(ip,end' ')
        return ip




def main():
    # get ips from web site
    proxy_pool = proxy_get()
    # test ips
    pool = ThreadPool()
    results = pool.map(proxy_test,proxy.address)
    pool.close()
    pool.join()
    # drop useless ips
    while None in results:
        results.remove(None)
    # save list
    with open('proxy_pool.json', 'w') as fp:
        json.dump(results,fp)
    # finish
    print('main ended')

    
    
    
if __name__ == '__main__':
    proxy = main()
