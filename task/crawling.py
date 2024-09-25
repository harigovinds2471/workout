import requests
from parsel import Selector

class WebCrawl:
    def __init__(self):
        self.base_url = "https://www.mytheresa.com"
        self.start_url = "https://www.mytheresa.com/euro/en/men/shoes"
        self.product_urls = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def fetch(self):
        url = self.start_url
        while url:
            print(f"Fetching {url}")
            response = requests.get(url)
            selector = Selector(text=response.text)

            product_urls_type1 = selector.xpath('//div[@class="list__container"]//div[contains(@class, "item") and contains(@class, "item--sale")]//a[contains(@class, "item__link")]/@href').getall()
            product_urls_type2 = selector.xpath('//div[@class="list__container"]//div[contains(@class, "item") and not(contains(@class, "item--sale"))]//a[contains(@class, "item__link")]/@href').getall()

            self.product_urls.extend([self.base_url + path for path in product_urls_type1 + product_urls_type2])

            next_page_url = selector.xpath("//a[contains(@class, 'pagination__item') and contains(@class, 'pagination__item__text') and @data-label='nextPage']/@href").get()            
            if next_page_url:
                url = self.base_url + next_page_url
            else:
                url = None

    def save_product_urls(self, filename="samples.txt"):
        with open(filename, "w") as file:
            for url in self.product_urls:
                file.write(url + "\n")

if __name__ == "__main__":
    crawler = WebCrawl()
    crawler.fetch()
    crawler.save_product_urls()
