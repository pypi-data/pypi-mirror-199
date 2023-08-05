import copy
import json
import re
import scrapy
from CarH.Utils import CPUtils



class AutohomeSpider(scrapy.Spider):
    name = 'autohome'
    # allowed_domains = ['autohome.com']
    # start_urls = ['https://dealer.autohome.com.cn/beijing/0/0/0/0/1/0/0/0.html#pvareaid=2113613']
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
    }
    protocol = 'https:'
    base_url = 'https://dealer.autohome.com.cn/'

    def start_requests(self):
        item = {}
        urls = [
            'https://dealer.autohome.com.cn/beijing/0/0/0/0/1/0/0/0.html#pvareaid=2113613',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,headers=self.headers,meta={'item':copy.deepcopy(item)})

    def parse(self, response):
        item = copy.deepcopy(response.meta['item'])
        links = response.xpath('//ul//li[@class="tit-row"]//a//@href').extract()
        title = response.xpath('//ul//li[@class="tit-row"]//a//span/text()').extract()
        for l,t in zip(links,title):
            url = self.protocol + l
            item['Dealer_Name'] = t
            yield scrapy.Request(url=url,headers=self.headers,meta={'item':copy.deepcopy(item)}, callback=self.trun_car)

        pass

    #跳转到车型报价
    def trun_car(self,response):
        item = copy.deepcopy(response.meta['item'])
        Dealer_Name_Carlink = response.xpath('//ul//li[@id="nav_1"]//a/@href').extract_first()
        #获取dealerId
        dealerId = re.findall(r'/(\d+)/', Dealer_Name_Carlink)[0]
        item['dealerId'] = dealerId
        Dealer_Name_Carlink = self.base_url + Dealer_Name_Carlink
        yield scrapy.Request(url=Dealer_Name_Carlink, headers=self.headers, meta={'item': copy.deepcopy(item)}, callback=self.get_TheId)

    #获取车型报价详情id
    def get_TheId(self,response):
        item = copy.deepcopy(response.meta['item'])
        links = response.xpath('//div[@class="brandtree-cont"]//dd/a/@href').extract()
        title = response.xpath('//div[@class="brandtree-cont"]//dd/a/text()').extract()
        for l, t in zip(links, title):
            seriesId = re.findall(r'b_(\d+)\.', l)[0]
            item['seriesId'] = seriesId
            # 车系名称
            item['seriesName'] = t
            url = f"https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getdealerspeclist&dealerId={item['dealerId']}&seriesId={item['seriesId']}"
            yield scrapy.Request(url=url, headers=self.headers, meta={'item': copy.deepcopy(item)},
                                 callback=self.get_details)

    # 获取车型报价详情字段
    def get_details(self,response):
        item = copy.deepcopy(response.meta['item'])
        json_data = json.loads(response.text)
        #是列表
        for data in json_data['result']:
            # 车型
            item['Car_type'] = data['groupName']
            for detial in data['list']:
                #车款
                item['specName'] = detial['specName']
                #指导价
                item['dealerMaxPrice'] = detial['dealerMaxPrice']
                #裸车价
                item['newsPrice'] = detial['newsPrice']
        yield item


    def closed(self, reason):
        '''
        用来传递信号来结束当前代理池的定时任务
        :param reason:
        :return:
        '''
        # 在爬虫关闭时被调用
        Utils = CPUtils()
        Utils.shutdown()
        print('爬虫关闭了！原因是:', reason)





