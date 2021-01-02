import scrapy
from scrapy.crawler import CrawlerProcess
import re
import pandas as pd
from IPython.display import display, HTML

dict = {    'Dönem':[], 
	    'DönemYıl':[], 
	    'Tarih':[],
	    'Birleşim':[],
	    'BirleşimURL':[],
	    'Tutanak':[]
	   }

records=pd.DataFrame(dict)

class URLSpider(scrapy.Spider):
	name = "recordsurl"
	def start_requests(self):
		urls = [
			'https://www.tbmm.gov.tr/tutanak/tutanaklar.htm',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parseYil)

	def parseYil(self, response):

		yilURL=response.css(".anaORTAsayfaBaslik a::attr(href)").extract()

		for yil in yilURL:
			yield scrapy.Request(url=yil, callback=self.parseBirlesim)
			print(yil)
			

	def parseBirlesim(self,response):
		parsingURL=re.findall('://www.tbmm.gov.tr/tutanak/donem([\w\-\.]+)/tutanak([\w\-\.]+).htm',response.url)
		donemNo=parsingURL[0][0]
		yilNo=parsingURL[0][1]
		birlesimURL=response.xpath('/html//a[contains (text(),"Birleşim")]/@href').extract()
		birlesimNo=response.xpath('/html//a[contains (text(),"Birleşim")]/text()').extract()
		birlesimNo=[no.split(".")[0] for no in birlesimNo]
		dates=response.xpath('//table[@cols="2"]/tr[*]/td[2]/text()').extract()
		dates=[date.split()[0] for date in dates]
		global records
		for i in range(len(birlesimURL)):
			record = {'Dönem':donemNo, 'DönemYıl':yilNo, 'Tarih':dates[i], 'Birleşim':birlesimNo[i],'BirleşimURL':birlesimURL[i]}
			records = records.append(record, ignore_index = True)
						

process = CrawlerProcess()
process.crawl(URLSpider)
process.start()

#pd.set_option('display.max_colwidth', -1)
display(records)
		
