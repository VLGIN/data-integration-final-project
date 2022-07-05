from scrapy import Spider
from crawler.items import CrawlerItem

from scrapy import Spider, Request
from w3lib.url import add_or_replace_parameter
import json


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["didongviet.vn"]
    start_urls = [
        "https://didongviet.vn/dien-thoai?p=1",
    ]

    def parse(self, response):
        # parse first page
        yield from self.parse_phone_list(response)
        # parse next pages
        for page in range(2, 10):
            url = add_or_replace_parameter(response.url, 'p', page)
            yield Request(url, callback=self.parse_phone_list)

    def parse_phone_list(self, response):
        phone_list = response.xpath(
            '//*[@id="maincontent"]/div[3]/div/div/div/div[3]/ol/li')
        for phone_card in phone_list:
            phone_info_url = phone_card.xpath(
                'div/div[2]/h3/a/@href').extract_first()
            yield Request(phone_info_url, self.parse_phone_info)

    def parse_phone_info(self, response):
        item = CrawlerItem()
        item['Đường dẫn'] = response.request.url
        item['Tiêu đề'] = response.xpath(
            '//*[@id="maincontent"]/div[2]/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]/h1/text()').extract_first()

        item['Giá bán'] = []
        price_list = response.xpath(
            '//*[@id="product-options-wrapper"]/div/div/div/label')
        for price in price_list:
            price_obj = {
                'Màu sắc': price.xpath('span[1]/text()').extract_first(),
                'Giá': price.xpath('span[2]/text()').extract_first()
            }
            item['Giá bán'].append(price_obj)

        item['Công nghệ màn hình'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[1]/div/span/text()').extract_first()
        item['Độ phân giải'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[2]/div/span/text()').extract_first()
        item['Màn hình rộng'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[3]/div/span/text()').extract_first()
        item['Mặt kính cảm ứng'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[4]/div/span/text()').extract_first()
        item['Camera sau'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[5]/div/span/text()').extract_first()
        item['Quay phim'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[6]/div/span/text()').extract_first()
        item['Đèn Flash'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[7]/div/span/text()').extract_first()
        item['Camera trước'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[8]/div/span/text()').extract_first()
        item['Videocall'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[9]/div/span/text()').extract_first()
        item['Hệ điều hành'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[10]/div/span/text()').extract_first()
        item['Chipset (hãng SX CPU)'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[11]/div/span/text()').extract_first()
        item['Chip đồ họa (GPU)'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[12]/div/span/text()').extract_first()
        item['RAM'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[13]/div/span/text()').extract_first()
        item['Bộ nhớ trong'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[14]/div/span/text()').extract_first()
        item['Bộ nhớ còn lại (khả dụng)'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[15]/div/span/text()').extract_first()
        item['Thẻ nhớ ngoài'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[16]/div/span/text()').extract_first()
        item['Mạng di động'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[17]/div/span/text()').extract_first()
        item['SIM'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[18]/div/span/text()').extract_first()
        item['Wifi'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[19]/div/span/text()').extract_first()
        item['GPS'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[20]/div/span/text()').extract_first()
        item['Bluetooth'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[21]/div/span/text()').extract_first()
        item['Cổng kết nối/sạc'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[22]/div/span/text()').extract_first()
        item['Jack tai nghe'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[23]/div/span/text()').extract_first()
        item['Thiết kế'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[24]/div/span/text()').extract_first()
        item['Chất liệu'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[25]/div/span/text()').extract_first()
        item['Kích thước'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[26]/div/span/text()').extract_first()
        item['Trọng lượng'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[27]/div/span/text()').extract_first()
        item['Loại pin'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[28]/div/span/text()').extract_first()
        item['Công nghệ pin'] = response.xpath(
            '//*[@id="product-attribute-specs-table"]/ul/li[29]/div/span/text()').extract_first()

        yield item
