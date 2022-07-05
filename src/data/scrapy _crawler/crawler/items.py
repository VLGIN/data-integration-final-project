# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    def __init__(self):
        super().__init__()
        self.fields['Đường dẫn'] = scrapy.Field()
        self.fields['Tiêu đề'] = scrapy.Field()
        self.fields['Giá bán'] = scrapy.Field()
        # specifications
        self.fields['Công nghệ màn hình'] = scrapy.Field()
        self.fields['Độ phân giải'] = scrapy.Field()
        self.fields['Màn hình rộng'] = scrapy.Field()
        self.fields['Mặt kính cảm ứng'] = scrapy.Field()
        self.fields['Camera sau'] = scrapy.Field()
        self.fields['Quay phim'] = scrapy.Field()
        self.fields['Đèn Flash'] = scrapy.Field()
        self.fields['Camera trước'] = scrapy.Field()
        self.fields['Videocall'] = scrapy.Field()
        self.fields['Hệ điều hành'] = scrapy.Field()
        self.fields['Chipset (hãng SX CPU)'] = scrapy.Field()
        self.fields['Chip đồ họa (GPU)'] = scrapy.Field()
        self.fields['RAM'] = scrapy.Field()
        self.fields['Bộ nhớ trong'] = scrapy.Field()
        self.fields['Bộ nhớ còn lại (khả dụng)'] = scrapy.Field()
        self.fields['Thẻ nhớ ngoài'] = scrapy.Field()
        self.fields['Mạng di động'] = scrapy.Field()
        self.fields['SIM'] = scrapy.Field()
        self.fields['Wifi'] = scrapy.Field()
        self.fields['GPS'] = scrapy.Field()
        self.fields['Bluetooth'] = scrapy.Field()
        self.fields['Cổng kết nối/sạc'] = scrapy.Field()
        self.fields['Jack tai nghe'] = scrapy.Field()
        self.fields['Thiết kế'] = scrapy.Field()
        self.fields['Chất liệu'] = scrapy.Field()
        self.fields['Kích thước'] = scrapy.Field()
        self.fields['Trọng lượng'] = scrapy.Field()
        self.fields['Loại pin'] = scrapy.Field()
        self.fields['Công nghệ pin'] = scrapy.Field()
