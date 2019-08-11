# -*- coding: utf-8 -*-
import scrapy

class Spider(scrapy.Spider):
        name = 'unsw_enrolment'

        start_urls = ['https://student.unsw.edu.au/summer', 'https://student.unsw.edu.au/enrol/change']
        custom_settings={ 'FEED_URI': "../../scrapedData.json",'FEED_FORMAT': 'json'}
        
        def parse(self, response):
            #extract raw data from website
            intent= "Enrollment.Basic.manage_enrolment"
            userquery = response.xpath("//h2[@class='header-content-section']/text()").extract()
            response = response.xpath("//div[@class='page-content-section-expand']").extract()
            new_response = []
            
            bad_char = ['<div class="page-content-section-expand">','</div>','<p>','</p>','\n','<strong>','</strong>','</a>','<li>','</li>','<ul>','</ul>','\xa0']
                                          
            #clean up data 
            for i in response:
                for x in bad_char:
                    i = i.replace(x,'').strip()
                                                                                                                                                
                new_response.append(i)

            row_data = zip(userquery,new_response)


            #merge items for export to JSON file
            for item in row_data:

                scraped_info ={
                                                                                                                                                                                                                                        'intent': intent,
                                                                                                                                                                                                                                        'userquery': item[0],
                                                                                                                                                                                                                                        'response': item[1],                                                                                                                                                                                            }
                yield scraped_info
