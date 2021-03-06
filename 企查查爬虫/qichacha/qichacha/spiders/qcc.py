# -*- coding: utf-8 -*-
import scrapy, re, os
import pandas as pd
from qichacha.items import QichachaItem

class QccSpider(scrapy.Spider):
    name = 'qcc'
    allowed_domains = ['qcc.com']
    start_urls = ['http://qcc.com/']

    def get_list(self, trs):
        ths = trs[0].xpath('.//th')
        li = []
        for i in range(1, len(trs), 2):
            dt = {}
            for j in range(len(ths)):
                if j == 1:
                    key = re.sub('\s', '', ths[1].xpath('.//text()').get())
                    if key == '':
                        key = re.sub('\s', '', ''.join(ths[1].xpath('.//span//text()').getall()))
                    value = trs[i].xpath('./td[2]//span[@class="seo font-14"]//text()').get()
                    dt.update({key: value})
                else:
                    key = re.sub('\s', '', ths[j].xpath('./text()').get())
                    if key == '':
                        key = re.sub('\s', '', ''.join(ths[j].xpath('.//text()').getall()))
                    value = re.sub('\s', '', trs[i].xpath('./td[{}]/text()'.format(j+1)).get())
                    if  value == '':
                        value = re.sub('\s', '', ''.join(trs[i].xpath('./td[{}]//text()'.format(j+1)).getall()))
                    dt.update({key: value})

            li.append(dt)
        return li

    def start_requests(self):
        # 目录
        excel = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'check.xlsx')
        firm_list = pd.read_excel(excel)
        for i in range(len(firm_list)):
            firm = firm_list.iloc[i,0]
            url = 'https://www.qcc.com/web/search?key={}'.format(firm)
            yield scrapy.Request(url, callback=self.get_firm_url)

    def get_firm_url(self, response):
        firm_url = response.xpath('.//div[@class="maininfo"]')[0].xpath('.//a/@href')[0].get()
        firm_token = re.search('firm/(.*?)\.html', firm_url).group(1)
        detail_url = 'https://www.qcc.com/cbase/{}'.format(firm_token)
        yield scrapy.Request(detail_url, callback=self.get_firm_detail)


    def get_firm_detail(self, response):
        Cominfo = response.xpath('.//section[@id="Cominfo"]//tr') 
        item = QichachaItem()
        item.fields['企业名称'] = scrapy.Item()
        item['企业名称'] = re.sub('\s', '', response.xpath('.//h1//text()').get())
        # 获取基本信息
        for tr in Cominfo:
            tds = tr.xpath('.//td')
            for i in range(0, len(tds), 2):
                field = re.sub('\s', '', tds[i].xpath('.//text()').get())
                try:
                    content = re.sub('\s', '', tds[i+1].xpath('.//h2//text()').get())
                except:
                    content = re.sub('\s', '', tds[i+1].xpath('.//text()').get())
                item.fields[field] = scrapy.Item()
                item[field] = content

        # 股东信息
        try:
            trs = response.xpath('.//div[@id="ipopartnerslist"]//tr')
            partnerslist = self.get_list(trs)
            item.fields['股东信息'] = scrapy.Item()
            item['股东信息'] = partnerslist
        except:
            trs = response.xpath('.//div[@id="partnerslist"]//tr')
            partnerslist = self.get_list(trs)
            item.fields['股东信息'] = scrapy.Item()
            item['股东信息'] = partnerslist

        # 高管信息
        try:
            trs = response.xpath('.//div[@id="ipoemployeeslist"]//tr')
            employeeslist = self.get_list(trs)
            item.fields['高管信息'] = scrapy.Item()
            item['高管信息'] =employeeslist
        except:
            trs = response.xpath('.//div[@id="employeeslist"]//tr')
            employeeslist = self.get_list(trs)
            item.fields['高管信息'] = scrapy.Item()
            item['高管信息'] =employeeslist
        
        yield item
