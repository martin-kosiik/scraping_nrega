!scrapy shell "http://quotes.toscrape.com/page/1/"

# table css selector
#  #form1 > div:nth-child(4) > center > table:nth-child(5)

# table xpath
# //*[@id="form1"]/div[3]/center/table[1]

#table = response.xpath('//*[@class="table table-striped"]')


# https://www.simplified.guide/scrapy/scrape-table

table = response.xpath('//*[@id="form1"]/div/table[2]')

table = response.xpath('//*[@id="form1"]/div//table')[3]

rows = table.xpath('//tr')[2:-3]
rows[2:50]
row = rows[10]

#http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=s&lflag=eng&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national&Digest=z3lVd7ic0u/yHHasXbssXA

district_name = row.xpath('td//text()')[1].extract()
district_link = row.xpath('td//@href').extract()[0]
district_census_code = row.xpath('td//text()')[2].extract()
no_villages = row.xpath('td//text()')[3].extract()
no_villages_with_code = row.xpath('td//text()')[4].extract()


{
'district_name': row.xpath('td//text()')[1].extract(),
'district_link': row.xpath('td//@href').extract()[0],
'district_census_code': row.xpath('td//text()')[2].extract(),
'no_villages': row.xpath('td//text()')[3].extract(),
'no_villages_with_code': row.xpath('td//text()')[4].extract()
}



# e.g., here is a problem with a village missing a census code
# http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=v&block_code=1737001&block_name=LAKHNADON&panchayat_code=1737001038&panchayat_name=DHANKAKDI&state_name=MADHYA%20PRADESH&state_code=17&district_name=SEONI&fin_year=2021-2022&source=national



try:
    village_census_code = row.xpath('td//text()')[2].extract()
except IndexError:
    village_census_code = 'missing'
except:
    village_census_code = "something else wrong"



# http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=b&district_code=1751&district_name=AGAR-MALWA&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national





class Test1Spider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ['mnregaweb4.nic.in']
    start_urls = ['http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=s&lflag=eng&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national&Digest=z3lVd7ic0u/yHHasXbssXA']

    def parse(self, response):
        table = response.xpath('//*[@id="form1"]/div//table')[3]
        rows = table.xpath('//tr')[3:-4]
        data = {}
        for row in rows:
            data.update(
            {
            'district_name': row.xpath('td//text()')[1].extract(),
        #    'district_link': row.xpath('td//@href').extract()[0],
            'district_census_code': row.xpath('td//text()')[2].extract(),
            'no_villages': row.xpath('td//text()')[3].extract(),
            'no_villages_with_code': row.xpath('td//text()')[4].extract()
            }
            )
        yield data



!scrapy crawl test1 -O dist_names.json

class Test1Spider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ['interpol.int']
    start_urls = ['https://www.interpol.int/notice/search/woa/1192802']

    def parse(self, response):
        table_rows = response.xpath('//*[contains(@class,"col_gauche2_result_datasheet")]//tr').extract()
        data = {}
        for table_row in table_rows:
            data.update({response.xpath('//td[contains(@class, "col1")]/text()').extract(): response.css('//td[contains(@class, "col2")]/text()').extract()})
        yield data




response.xpath('//*/head/title/text()').get()

"http://mnregaweb4.nic.in/netnrega/show_censuscode.aspx?page=s&lflag=eng&state_name=MADHYA%20PRADESH&state_code=17&fin_year=2021-2022&source=national&Digest=z3lVd7ic0u/yHHasXbssXA"


import json
import os
import pandas as pd
os.chdir(r'C:\Users\marti\OneDrive\Plocha\research_projects\scraping_nrega\scrapy_spiders\tutorial')

os.listdir()
# Opening JSON file
f = open('all_levels_names_and_codes_2.json',)

# returns JSON object as
# a dictionary
data = json.load(f)

f.close()


village_names_list = [x['village_name'] for x in data if x['data_level'] == 'village']
village_code_list = [x['village_census_code'] for x in data if x['data_level'] == 'village']
panchayat_url_list = [x['panchayat_url'] for x in data if x['data_level'] == 'village']



village_codes_df = pd.DataFrame({'village_name': village_names_list,
                                 'village_census_code': village_code_list,
                                 'panchayat_url': panchayat_url_list})



panch_url = village_codes_df['panchayat_url'][0]

village_codes_df['panchayat_name'] = village_codes_df['panchayat_url'].str.extract('&panchayat_name=([^&]+)&')
village_codes_df['panchayat_code'] = village_codes_df['panchayat_url'].str.extract('&panchayat_code=(\d+)&')

village_codes_df['block_name'] = village_codes_df['panchayat_url'].str.extract('&block_name=([^&]+)&')
village_codes_df['block_code'] = village_codes_df['panchayat_url'].str.extract('&block_code=(\d+)&')

village_codes_df['district_name'] = village_codes_df['panchayat_url'].str.extract('&district_name=([^&]+)&')



district_names_list = [x['district_name'] for x in data if x['data_level'] == 'district']
district_code_list = [x['district_census_code'] for x in data if x['data_level'] == 'district']


district_codes_df = pd.DataFrame({'district_name': district_names_list,
                                 'district_census_code': district_code_list})

district_codes_df.dtypes

village_codes_df.dtypes

village_codes_df.join(district_codes_df, how='left', on='district_name')

village_codes_df = pd.merge(village_codes_df, district_codes_df, how='left', on='district_name')


village_codes_df['state_name'] = village_codes_df['panchayat_url'].str.extract('&state_name=([^&]+)&')
village_codes_df['state_code'] = village_codes_df['panchayat_url'].str.extract('&state_code=(\d+)&')






panch_url.extract('&block_code=\d+&')

village_names_list.__len__()
village_code_list.__len__()
data
