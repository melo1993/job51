# -*- coding: utf-8 -*-
#encoding=utf-8

import string
import sys
from urllib import quote
import re
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
import items
reload(sys)
sys.setdefaultencoding('utf-8')

positionsname = ['java',
                 '销售',
                 '会计',
                 '房地产',
                 '行政',
                 'php',
                 '平面设计',
                 '外贸',
                 '产品经理',
                 '财务',
                 '人事',
                 '金融']

baseurl = 'http://search.51job.com/'

class job51Spider(Spider):
    name = 'job51'
    allowed_domains = []
    start_urls=[]
    for positions in positionsname:
      urlkeyword = quote(positions, 'UTF-8')
      start_urls.append(baseurl + 'list/000000,000000,0000,00,9,99,'+urlkeyword +',2,1.html?lang=c&degreefrom=99&stype=&workyear=99&cotype=99&jobterm=99&companysize=99&radius=-1&address=&lonlat=&postchannel=&list_type=&ord_field=&curr_page=&dibiaoid=0&landmark=&welfare=')

    def parse(self, response):
        sel = Selector(response)
        pagecountObj=sel.xpath('//html/body/div[2]/div[6]/div/div/div/span[1]/text()').extract()[0]
        pagecount=str(pagecountObj)
        pagecount=string.replace(pagecount,'共','',-1)
        pagecount=string.replace(pagecount,'页，到第','',-1)
        keywordobj=sel.xpath(".//*[@id='kwdselectid']/@value").extract()[0];
        keyword=str(keywordobj);
        for i in range(1, int(pagecount)+1):
            pageurl=baseurl+'jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword='+quote(keyword, 'UTF-8')+'&keywordtype=2&curr_page='+str(i)+'&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9'
            yield scrapy.Request(pageurl, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        joblist = sel.xpath(".//*[@id='resultList']/div[@class='el']/p/span/a/@href").extract();
        companynames=sel.xpath(".//*[@id='resultList']/div[@class='el']/span/a");
        for index,job in enumerate(joblist):
            joburl=str(job)
            companyname=companynames[index]
            companynametext=companyname.xpath('string(.)').extract()[0]
            item = items.Job51Item()
            item["link"]=joburl
            item["companyname"] = companynametext
            yield scrapy.Request(joburl, meta={'item': item}, callback=self.parse_job)

    def parse_job(self, response):
        item = response.meta['item']
        sel = Selector(response)
        id=str(sel.xpath(".//*[@id='hidJobID']/@value").extract()[0])
        name= str(sel.xpath(".//div[@class='cn']/*[local-name() = 'h1']/text()").extract()[0])
        city= str(sel.xpath(".//div[@class='cn']/span/text()").extract()[0])
        try:
            salary = str(sel.xpath(".//div[@class='cn']/strong/text()").extract()[0])
        except:
            salary = ''
        try:
            time_range=str(sel.xpath(".//*[@class='i1']/parent::*/text()").extract()[0])
        except:
            time_range = ''

        try:
            edu=str(sel.xpath(".//*[@class='i2']/parent::*/text()").extract()[0])
        except:
            edu = ''

        try:
            count=str(sel.xpath(".//*[@class='i3']/parent::*/text()").extract()[0])
        except:
            count = ''

        try:
            updatetime=str(sel.xpath(".//*[@class='i4']/parent::*/text()").extract()[0])
        except:
            updatetime = ''

        try:
            lang=str(sel.xpath(".//*[@class='i5']/parent::*/text()").extract()[0])
        except:
            lang = ''

        companydescription = sel.xpath(".//div[@class='tmsg inbox']/text()").extract()
        allDescs = ""
        for allitem in companydescription:
            allDescs = allDescs + str(allitem)
        allDescs = string.replace(allDescs, "\t", "", -1)
        allDescs = string.replace(allDescs, "\r\n", "", -1)

        benefitlist=sel.xpath(".//*[@class='jtag inbox']/p/span/text()").extract()
        benefit=""
        for benfititem in benefitlist:
            benefit=benefit+str(benfititem)+","

        alllist=sel.xpath(".//div[@class='bmsg job_msg inbox']/text()").extract()
        allDesc=""
        for allitem in alllist:
            allDesc=allDesc+str(allitem)
        respstart=allDesc.rfind("职位描述:")
        if respstart==-1:
            respstart=0
        respend=allDesc.rfind("任职要求：")
        if respend==-1:
            respend=allDesc.rfind("岗位要求：")
        if respend==-1:
            respend=allDesc.rfind("任职资格：")
        if respend==-1:
            respend=len(allDesc)-1
        responsibility=str(allDesc[respstart:respend])
        responsibility=string.replace(responsibility,"\t","",-1)
        responsibility=string.replace(responsibility,"\r\n","",-1)
        qualstart=allDesc.rfind("任职要求：")
        if qualstart==-1:
            qualstart=allDesc.rfind("岗位要求：")
        if qualstart==-1:
            qualstart=allDesc.rfind("任职资格：")
        if qualstart==-1:
            qualstart=len(allDesc)
        qualend=len(allDesc)+1
        qualification=str(allDesc[qualstart:qualend])
        qualification=string.replace(qualification,"\t","",-1)
        qualification=string.replace(qualification,"\r\n","",-1)

        item["email"] = ''
        rex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
        try:
            email = str(sel.xpath(".//div[@class='bmsg job_msg inbox']/text()").extract());
        except:
            email = ''
        xx = re.compile(rex)
        for j in xx.findall(email):
            item["email"] = j

        item["contact_phonenum"] = ''
        rex_num =r'1[358]\d{9}|147\d{8}|(0\d{2,3})?\d{7,8}'
        #rex_num = r'(^1\d{10})'
        try:
            contact_phonenum = str(sel.xpath(".//div[@class='bmsg job_msg inbox']/text()").extract());
        except:
            contact_phonenum = ''
        xx = re.compile(rex_num)
        for b in xx.findall(contact_phonenum):
            item['contact_phonenum'] =b

        companylist=sel.xpath("//html/body/div[2]/div[2]/div[2]/div/div[1]/p[1]/a/@href").extract();
        for companyurl in companylist:
            companyurls = str(companyurl)
            item['linker'] = companyurls
            yield scrapy.Request(companyurls, meta={'item': item}, callback=self.parse_company)



        item["id"] = id
        item["name"] = name
        item["city"] = city
        item["salary"] = salary
        item["time_range"] = time_range
        item["edu"] = edu
        item["count"] = count
        item["updatetime"] = updatetime
        item["lang"] = lang
        item["benefit"] = benefit
        item["companydescription"] = allDescs
        item["responsibility"] = responsibility
        item["qualification"] = qualification

    def parse_company(self, response):
        item = response.meta['item']
        sel = Selector(response)
        address= str(sel.xpath(".//p[@class='fp']/text()").extract()[1])
        address = string.replace(address, "\t", "", -1)
        address = string.replace(address, "\r\n", "", -1)

        item["address"] = address


        yield item


