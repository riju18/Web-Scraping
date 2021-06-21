import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']  # don't use http protocol
    '''
    In start_urls scrapy adds 'http' by default. 
    So we need to manually change if it 'https'.
    '''
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')  # crawl each link
        for country in countries:
            name = country.xpath('.//text()').get()  # name of the link
            link = country.xpath('.//@href').get()  # href of the link

            # yield {
            #     "country-name": name,
            #     "country-link": link,
            # }

            # absolute_url = f"https://www.worldometers.info{link}"
            # or,
            absolute_url = response.urljoin(link)
            yield scrapy.Request(url=absolute_url,
                                 callback=self.parse_country,
                                 meta={'country_name': name})  # meta is used to pass additional info

    def parse_country(self, response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover "
                              "table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                "name": name,
                "year": year,
                "population": population
            }
