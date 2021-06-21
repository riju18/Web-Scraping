import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a",)),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[2]",))),
    )

    def parse_item(self, response):
        yield {
            "title": response.xpath("//div[@class='title_wrapper']/h1/text()[1]").get(),
            "year": response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get(),
        }
