from scrapy.spiders import CrawlSpider
import re
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrpy.items import NoutItem


class NoutSpider(CrawlSpider):
    name = 'nout'
    allowed_domains = ['notik.ru']
    start_urls = ['https://www.notik.ru/index/notebooks.htm?srch=true&full=&f117=5650']
    default_headers ={}
    def parse(self, response):
        for card in response.xpath("//tr[@class='hide-mob']//a/@href"):
            yield response.follow(card, callback=self.parse_nout_notik)
        for page in response.xpath("//div[@class='paginator align-left']//a/@href"):
            yield response.follow(page, callback=self.parse)

    def parse_nout_notik(self, response):
        item = NoutItem()
        column1=response.xpath("//table[@class='parametersInCard column']")[0]
        column2=response.xpath("//table[@class='parametersInCard column']")[1]
        price = column2.xpath("//*[.='Цена:']/parent::td/following::td[1]")
        price = price.xpath("//span[@itemprop='price']/text()").get().split()

        item['url'] = response.url
        item['date'] = datetime.now().strftime("%d.%m.%Y %H:%M")  
        item['name']=re.sub(r'Ноутбук','',response.xpath("//h1[@class='goodtitlemain']/text()").get()).strip()
        item['processor'] = column1.xpath("//*[.='Процессор:']/parent::td/following::td[1]/text()").get().replace("\xa0", " ").strip()
        item['core'] = int(column1.xpath("//*[.='Количество ядер:']/parent::td/following::td[1]/text()").get().strip())
        item['mhz'] = round(float(re.findall(r'([\d.]+?)\sГГц', item['processor'])[0]) * int(item['core']),1)
        item['ram'] = int(column1.xpath("//*[.='Оперативная память:']/parent::td/following::td[1]/text()").get().split(' ')[0])
        item['screen'] = float(column1.xpath("//*[.='Экран:']/parent::td/following::td[1]/text()").get().split('"')[0])
        item['price'] = int("".join(price))

        return item

    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
                url, callback=self.parse, headers=self.default_headers
                )

class NoutSpider_2(CrawlSpider):
    name = 'nout2'
    allowed_domains = ['sp-computer.ru']
    start_urls = ['https://www.sp-computer.ru/catalog/noutbuki/']
    hurl = "https://www.sp-computer.ru/"
    default_headers ={}
    def parse(self, response):
        nout_card = "//div[@class='col-xs-12']//div[@class='product-item-title']//a/@href"
        for card in response.xpath(nout_card):
            yield response.follow(card, callback=self.parse_nout)
        next_page_css = '.bx-pag-next a ::attr(href)'
        for nextpage_link in response.css(next_page_css):
            yield response.follow(url=nextpage_link, callback=self.parse)

    def parse_nout(self, response):
        item = NoutItem()
        freq_mhz = 0.0
        freq_core = 1.0
        proc_type = response.xpath("//div[.='Модель процессора' or .='Процессор']/following-sibling::div/text()").get().strip()
        proc_core = response.xpath("//div[.='Характеристики процессора']/following-sibling::div/text()").get().strip()
        proc = re.findall(r'(\d+[\.]?[\d+]?) ?[\D]+(\d?)', proc_core)
        price = response.xpath("//td[@class='price']/span/text()").get().strip()
        if proc[0][0]:
            freq_mhz=float(proc[0][0])
        if proc[0][1]:
            freq_core=float(proc[0][1])

        item['url'] = response.url
        item['date'] = datetime.now().strftime("%d.%m.%Y %H:%M")  
        item['name']=re.sub(r'Ноутбук?','',response.xpath("//div[@class='head_title pad_mobi']/h1/text()").get().split(',')[0]).strip()
        item['processor'] = proc_type+" "+ proc_core
        item['core'] = freq_core
        item['mhz'] = round(freq_mhz*freq_core,1)
        item['ram'] = response.xpath("//div[.='Оперативная память']/following-sibling::div/text()").get().strip().split(" ")[0]
        item['screen'] = response.xpath("//div[.='Диагональ экрана в дюймах']/following-sibling::div/text()").get().strip()
        item['price'] = int(re.sub(r'\D?', '', price))
        return item
 
    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
                url, callback=self.parse, headers=self.default_headers
                )

class NoutSpider_3(CrawlSpider):
    name = 'nout3'
    allowed_domains = ['pc-arena.ru']
    start_urls = ['https://pc-arena.ru/catalog/brendovye-tovary/noutbuki/filter/price-base-to-297276.20/prm_5093-from-13.9-to-15.5/prm_5101-to-35/apply/']
    hurl = "https://www.pc-arena.ru/"
    default_headers ={}
    def parse(self, response):
        nout_card = "//div[@class='catalog_block items block_list']//div[@class='item-title']//a/@href"
        for card in response.xpath(nout_card):
            yield response.follow(card, callback=self.parse_nout)
        next_page = "//div[@class='bottom_nav block']//li[@class = 'flex-nav-next ']//a/@href"
        for page in response.xpath(next_page):
            yield response.follow(page, callback=self.parse)

    def parse_nout(self, response):
        item = NoutItem()
        proc_mhz = re.sub(r"\s?","",response.xpath("//tr[td[. ='Тактовая частота']]/td[2]/text()").get())
        if "МГц" in proc_mhz:
            proc_mhz = float(re.findall(r"(\d+[\.]?[\d+]?)",proc_mhz)[0])/1000

        item['url'] = response.url
        item['date'] = datetime.now().strftime("%d.%m.%Y %H:%M")  
        item['name'] = re.sub(r'Ноутбук?','',response.xpath("//div[@class='product_name']/text()").get()).strip()
        item['processor'] = response.xpath("//tr[td[. ='Модель процессора']]/td[2]/text()").get() + " " + str(proc_mhz) + " ГГц"
        item['core'] = int(response.xpath("//tr[td[. ='Количество ядер']]/td[2]/text()").get())
        item['mhz'] = round(proc_mhz*item['core'],1)
        item['ram'] = int(re.findall(r"(\d)",response.xpath("//tr[td[. ='Объём памяти']]/td[2]/text()").get())[0])
        item['screen'] = float(re.findall(r"(\d+[\.]?[\d+]?)",response.xpath("//tr[td[. ='Диагональ экрана']]/td[2]/text()").get())[0])
        item['price'] = int(response.xpath("//div[@class='prices_block']//div[@class='price']/@data-value").get())
        return item
 
    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
                url, callback=self.parse, headers=self.default_headers
                )

process = CrawlerProcess(get_project_settings())
process.crawl(NoutSpider)
process.crawl(NoutSpider_2)
process.crawl(NoutSpider_3)
process.start() # the script will block here until all crawling jobs are finished