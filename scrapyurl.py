import scrapy
from scrapy.crawler import CrawlerProcess
import re
import pandas as pd
from IPython.display import display, HTML
import datetime

from Database.parse import *
from Database.storeMongo import *
from Database.storeMySql import *

# Creating databases
db_name = "testdatabase"

# MongoDB
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongoDb, TutanakT, OturumT, KonusmaT = mConnectDB(my_client, "TBMMDatabase")

# MySql
mySqlDB = connectToDB(db_name)
storeMilletvekili(mySqlDB, "BASKAN", "BASKENT", 0)

dict = {'Dönem': [],
        'DönemYıl': [],
        'Tarih': [],
        'Birleşim': [],
        'BirleşimURL': [],
        'Tutanak': []
        }

records = pd.DataFrame(dict)


class URLSpider(scrapy.Spider):
    name = "recordsurl"

    def start_requests(self):
        urls = [
            'https://www.tbmm.gov.tr/tutanak/tutanaklar.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseYil)


    def parseYil(self, response):

        yilURL = response.css(".anaORTAsayfaBaslik a::attr(href)").extract()

        for yil in yilURL:
            yield scrapy.Request(url=yil, callback=self.parseBirlesim)
            print(yil)


    def parseBirlesim(self, response):
        parsingURL = re.findall('://www.tbmm.gov.tr/tutanak/donem([\w\-\.]+)/tutanak([\w\-\.]+).htm', response.url)
        donemNo = parsingURL[0][0]
        yilNo = parsingURL[0][1]
        birlesimURL = response.xpath('/html//a[contains (text(),"Birleşim")]/@href').extract()
        birlesimNo = response.xpath('/html//a[contains (text(),"Birleşim")]/text()').extract()
        birlesimNo = [no.split(".")[0] for no in birlesimNo]
        dates = response.xpath('//table[@cols="2"]/tr[*]/td[2]/text()').extract()
        dates = [datetime.datetime.strptime(date.split()[0], '%Y.%m.%d') for date in dates]
        global records
        for i in range(len(birlesimURL)):
            record = {'Dönem': donemNo, 'DönemYıl': yilNo, 'Tarih': dates[i], 'Birleşim': birlesimNo[i],
                      'BirleşimURL': birlesimURL[i]}
            records = records.append(record, ignore_index=True)
			# MySql store Tutanak
			TutanakID = storeTutanak(mySqlDB, donemNo, yilNo, dates[i], birlesimNo[i], birlesimURL[i])
			yield scrapy.Request(url=birlesimURL[i], TutanakID=TutanakID, callback=self.parseTutanak)


	def parseTutanak(self, response):
		fileName = response.url
		fileName = fileName.replace("/", "_")
		fileName = fileName.replace(".", "")
		fileName = fileName.replace(":", "")
		fileName = fileName + ".html"

		if (response.css(".anaORTAsayfa").extract()) is None or len(response.css(".anaORTAsayfa").extract()) == 0:
			if (response.css(".Section1").extract()) is None or len(response.css(".Section1").extract()) == 0:
				tutanak = response.css(".WordSection1").extract()
			else:
				tutanak = response.css(".Section1").extract()

		else:
			tutanak = response.css(".anaORTAsayfa").extract()

		if tutanak is None:
			tutanak = response

		tutanak = ''.join(tutanak)
		tutanak = remove_html_markup(tutanak)
		tutanak = tutanak.replace('\xa0', '')
		tutanak = tutanak.replace("\n\n", " ")
		tutanak = tutanak.replace("  ", " ")
		# MongoDB store Tutanak
		mStoreTutanak(TutanakT, response.TutanakID, tutanak)
		sendTutanakToDB(OturumT, KonusmaT, mySqlDB, tutanak, response.TutanakID)


process = CrawlerProcess()
process.crawl(URLSpider)
process.start()

# pd.set_option('display.max_colwidth', -1)
display(records)