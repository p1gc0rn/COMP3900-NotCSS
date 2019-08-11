# -*- coding: utf-8 -*-
import scrapy

class DatesSpider(scrapy.Spider):
    name = 'dates'
    allowed_domains = ['https://student.unsw.edu.au/enrolment-dates']
    start_urls = ['https://student.unsw.edu.au/enrolment-dates/']
    custom_settings={ 'FEED_URI': "../../scrapedData.json",'FEED_FORMAT': 'json'}

    def parse(self, response):
        #extract data
        calendar = response.xpath("//h3/a/text()").extract()
        date = response.xpath("//div[@class='date-created']/text()").extract()
        info = response.xpath("//p/text()").extract()
        
        #clean up
        bad_chars = ['\n','\xa0',' ']
        new_info = []
        info = info[8:19]

        for i in info:
            for x in bad_chars:
                i = i.strip(x)
            
            new_info.append(i)
       
        row_data = zip(calendar,date,info)

        #merge the scraped data          
        for item in row_data:

            scraped_info ={
                    'calendar': item[0],
                    'date': item[1],
                    'info': item[2] ,

            }

            yield scraped_info


