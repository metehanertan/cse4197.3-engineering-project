import scrapy


class TutanakSpider(scrapy.Spider):
    name = "tutanak"

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
            

    def parseBirlesim(self,response):

    	birlesimURL=response.xpath('/html//a[contains (text(),"Birleşim")]/@href').extract()
    	for birlesim in birlesimURL:
    	    yield scrapy.Request(url=birlesim, callback=self.parseTutanak)

    def parseTutanak(self,response):
        fileName=response.url
        fileName=fileName.replace("/", "_")
        fileName=fileName.replace(".", "")
        fileName=fileName.replace(":", "")
        fileName=fileName + ".html"

        if (response.css(".anaORTAsayfa").extract()) is None or len(response.css(".anaORTAsayfa").extract()) == 0:
            if(response.css(".Section1").extract()) is None or len(response.css(".Section1").extract()) == 0:
                tutanak = response.css(".WordSection1").extract()
            else:
                tutanak = response.css(".Section1").extract()

        else:
            tutanak = response.css(".anaORTAsayfa").extract()
        
        if tutanak is None:
            tutanak=response

        tutanak=''.join(tutanak)

        file=open(fileName,"w", encoding="utf-8")
        file.write(tutanak)
        file.close()
