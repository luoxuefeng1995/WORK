# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import NewHouseItem, EsfHouseItem

class SfwSpiderSpider(scrapy.Spider):
    name = 'sfw_spider'
    # allowed_domains = ['ddddd']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath('//div[@id="c02"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            province_name = province_td.xpath('.//text()').extract_first()
            province_name = re.sub(r'\s','',province_name)
            if province_name:
                province = province_name
            if province == '其它':#(不爬取其它国的)
                continue
            city_td = tds[1]
            city_list = city_td.xpath('.//a')
            for i in city_list:
                city = i.xpath('.//text()').extract_first()
                city_url = i.xpath('.//@href').extract_first()

                url_module = city_url.split('//')
                scheme = url_module[0]
                domain = url_module[1]
                if "bj." in domain:
                    newhouse_url = 'https://newhouse.fang.com/house/s/'
                    esf_url = 'https://esf.fang.com'
                else:
                    newhouse_url = scheme + '//' + 'newhouse' + domain + 'house/s/'
                    esf_url = scheme + '//' + 'esf' + domain

                # print("城市：%s%s"%(province,city))
                # print("新房链接：%s"%newhouse_url)
                # print("二手房链接：%s"%esf_url)
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={'meta': (province, city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esfhouse, meta={'meta': (province, city)})
                break
            break
    def parse_newhouse(self, response):
        province, city = response.meta.get('meta')
        lis = response.xpath('//div[contains(@class, "nl_con")]/ul/li')
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first()
            if name:
                name = name.strip()

            house_type = li.xpath('.//div[contains(@class,"house_type")]/a/text()').extract()
            house_type = list(map(lambda x:re.sub(r'\s', "", x), house_type))

            rooms = list(filter(lambda x:x.endswith("居"), house_type))

            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").extract())
            area = re.sub(r"\s|/|－", "", area)

            address = li.xpath(".//div[@class='address']/a/@title").extract_first()

            district = "".join(li.xpath('.//div[@class="address"]/a//text()').extract())
            district = re.search(r".*\[(.+)\].*", district)
            if district:
                district = district.group(1)

            sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").extract_first()

            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").extract())
            price = re.sub(r"\s|广告", "", price)

            detail_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').extract_first()
            if detail_url:
                detail_url = 'https' + detail_url
            new = "newhouse"

            item = NewHouseItem(province=province, city=city, name=name, rooms=rooms, area=area, new=new,
                                price=price, address=address, sale=sale, district=district, detail_url=detail_url)

            yield item
        next_url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_newhouse, meta={'meta': (province, city)})


    def parse_esfhouse(self, response):
        province, city = response.meta.get('meta')
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:

            item = EsfHouseItem()

            item['province'] = province

            item['city'] = city

            item['name'] = dl.xpath('.//p[@class="add_shop"]/a/@title').extract_first()

            item['address'] = dl.xpath('.//p[@class="add_shop"]/span/text()').extract_first()

            item['price'] = ''.join(dl.xpath('.//span[@class="red"]//text()').extract())

            item['per_price'] = dl.xpath('./dd[@class="price_right"]/span[not(@class)]/text()').extract_first()

            detail_url = dl.xpath('.//h4[@class="clearfix"]/a/@href').extract_first()
            if detail_url:
                item['detail_url'] = response.urljoin(detail_url)

            item['old'] = "esfhouse"


            lis = dl.xpath('.//p[@class="tel_shop"]//text()').extract()

            lis = list(map(lambda x:re.sub(r'\s', '', x), lis))
            for i in lis:
                if "厅" in i:
                    item['rooms'] = i
                elif "㎡" in i:
                    item['area'] = i
                elif "层" in i:
                    item['floor'] = i
                elif "向" in i:
                    item['toward'] = i
                elif "年" in i:
                    item['year'] = i

            yield item

        next_url = response.xpath('//div[@id="list_D10_15"]//a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)

            yield scrapy.Request(url=next_url, callback=self.parse_esfhouse, meta={'meta': (province, city)})





