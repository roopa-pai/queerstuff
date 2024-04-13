
import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class EventSpider(scrapy.Spider):
    name = 'event_spider'
    start_urls = ['https://biberlin.de/events/']

    def parse(self, response):
        events = response.css('article.mec-event-article')
        for event in events:
            image_url = event.css('img::attr(src)').get()
            title = event.css('h3.mec-event-title a::text').get()
            date = event.css('span.mec-start-date-label::text').get()
            location = event.css('div.mec-venue-details span::text').get()
            description = event.css('div.mec-event-description::text').get()
            url = event.css('h3.mec-event-title a::attr(href)').get()

            yield {
                'image_url': image_url,
                'title': title.strip() if title else None,
                'date': date.strip() if date else None,
                'location': location,
                'description': description,
                'url': url
            }

def run_spider():
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result.json')

    process = CrawlerProcess(settings)
    process.crawl(EventSpider)
    process.start()
    return process.join()

if __name__ == "__main__":
    run_spider()