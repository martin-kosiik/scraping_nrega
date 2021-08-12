import scrapy


class Test1Spider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ['mnregaweb4.nic.in']
    start_urls = ['http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=s&lflag=eng&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national&Digest=z3lVd7ic0u/yHHasXbssXA']

    def parse(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[5:-3]
        for row in rows:
            yield {'district_name': row.xpath('td//text()')[1].extract(),
                    'district_link': row.xpath('td//@href').extract()[0],
                    'district_census_code': row.xpath('td//text()')[2].extract(),
                    'no_villages': row.xpath('td//text()')[3].extract(),
                    'no_villages_with_code': row.xpath('td//text()')[4].extract()}


class TestBlockSpider(scrapy.Spider):
    name = 'test_block'
    allowed_domains = ['mnregaweb4.nic.in']
    start_urls = ['http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=b&district_code=1751&district_name=AGAR-MALWA&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national']

    def parse(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[5:-3]
        for row in rows:
            yield {'block_name': row.xpath('td//text()')[1].extract(),
                    'block_link': row.xpath('td//@href').extract()[0],
                    'block_census_code': row.xpath('td//text()')[2].extract(),
                    'no_villages': row.xpath('td//text()')[3].extract(),
                    'no_villages_with_code': row.xpath('td//text()')[4].extract()}


class TestFullSpider(scrapy.Spider):
    name = 'test_full'
    allowed_domains = ['mnregaweb4.nic.in']
    start_urls = ['http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=s&lflag=eng&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national&Digest=z3lVd7ic0u/yHHasXbssXA']

    def start_requests(self):
        urls = [
            'http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=s&lflag=eng&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national&Digest=z3lVd7ic0u/yHHasXbssXA',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_dist)

    def parse_dist(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[5:-3]
        dist_link_list = []
        for row in rows:
            dist_link =  row.xpath('td//@href').extract()[0]
            dist_link_list.append(dist_link)
            yield {'data_level': 'district',
                    'district_name': row.xpath('td//text()')[1].extract(),
                    'district_link': dist_link,
                    'district_census_code': row.xpath('td//text()')[2].extract(),
                    'no_villages': row.xpath('td//text()')[3].extract(),
                    'no_villages_with_code': row.xpath('td//text()')[4].extract()}
        for link in dist_link_list:
            #yield Request(link, callback=self.parse_block)
            yield response.follow(link, callback=self.parse_block)


    def parse_block(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[5:-3]
        block_link_list = []
        for row in rows:
            block_link =  row.xpath('td//@href').extract()[0]
            block_link_list.append(block_link)

            yield {'data_level': 'block',
                    'block_name': row.xpath('td//text()')[1].extract(),
                    'block_link': block_link,
                    'block_census_code': row.xpath('td//text()')[2].extract(),
                    'no_villages': row.xpath('td//text()')[3].extract(),
                    'no_villages_with_code': row.xpath('td//text()')[4].extract()}
        for link in block_link_list:
            #yield Request(link, callback=self.parse_block)
            yield response.follow(link, callback=self.parse_panchayat)

    def parse_panchayat(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[5:-3]
        panch_link_list = []
        for row in rows:
            panch_link =  row.xpath('td//@href').extract()[0]
            panch_link_list.append(panch_link)

            yield {'data_level': 'panchayat',
                    'panch_name': row.xpath('td//text()')[1].extract(),
                    'panch_link': panch_link,
                    'no_villages': row.xpath('td//text()')[2].extract(),
                    'no_villages_with_code': row.xpath('td//text()')[3].extract()}
        for link in panch_link_list:
            yield response.follow(link, callback=self.parse_village)

    def parse_village(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[5:-3]
        for row in rows:
            try:
                village_census_code = row.xpath('td//text()')[2].extract()
            except IndexError:
                village_census_code = 'missing'
            except:
                village_census_code = "something else wrong"

            yield {'data_level': 'village',
                    'village_name': row.xpath('td//text()')[1].extract(),
                    'village_census_code': village_census_code,
                    'panchayat_url': response._url}
