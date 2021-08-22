import urllib
import scrapy
from scrapy import FormRequest, Request
#import scraper_helper as sh
from scrapy.shell import inspect_response
from scrapy.crawler import CrawlerProcess


def generate_form(response, level='state', state_value='17', district_value='0',
                    block_value='0', panchayat_value='0', gs_date_value='0'):
    __VIEWSTATE = response.xpath('//*[@name="__VIEWSTATE"]/@value').get()
    __EVENTTARGET = response.xpath('//*[@name="__EVENTTARGET"]/@value').get()
    __EVENTARGUMENT = response.xpath('//*[@name="__EVENTARGUMENT"]/@value').get()
    __VIEWSTATEENCRYPTED = response.xpath('//*[@name="__VIEWSTATEENCRYPTED"]/@value').get()
    __VIEWSTATEGENERATOR = response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').get()
    __EVENTVALIDATION = response.xpath('//*[@name="__EVENTVALIDATION"]/@value').get()

    __SCROLLPOSITIONX = '0'
    __SCROLLPOSITIONY = '0'
    __EVENTTARGET = 'ctl00$ContentPlaceHolder1$ddl'+level


    form = {
        'ctl00$ScriptManager1': 'ctl00$UpdatePanel1|ctl00$ContentPlaceHolder1$ddl'+level,
        '__LASTFOCUS': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        '__EVENTTARGET': __EVENTTARGET if __EVENTTARGET else '',
        '__EVENTARGUMENT': __EVENTARGUMENT if __EVENTARGUMENT else '',
        '__VIEWSTATEENCRYPTED': __VIEWSTATEENCRYPTED,
        '__EVENTVALIDATION': __EVENTVALIDATION,
        '__SCROLLPOSITIONX': __SCROLLPOSITIONX,
        '__SCROLLPOSITIONY': __SCROLLPOSITIONY,
        '__ASYNCPOST': 'false',
    #    '__RequestVerificationToken': __RequestVerificationToken,
    #    '__dnnVariable': __dnnVariable,
        'ctl00$ContentPlaceHolder1$ddlstate': state_value,
        'ctl00$ContentPlaceHolder1$ddldistrict': district_value,
        'ctl00$ContentPlaceHolder1$ddlBlock': block_value,
        'ctl00$ContentPlaceHolder1$ddlPanchayat': panchayat_value,
        'ctl00$ContentPlaceHolder1$ddlGSDate': gs_date_value,
        'ctl00$ContentPlaceHolder1$ddlselect': '0'
    }
    return form



class AspxSpider(scrapy.Spider):
    name = 'sa_aspx'
    start_urls = ['https://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng']

    custom_settings = {
            'FEED_URI': 'file://%(data_dir_path)s/sa_scraped_data.csv',
            'FEED_FORMAT': 'csv',
        #    'HTTPCACHE_ENABLED': True,
        #    'POSTSTATS_INTERVAL': 200
        }

    def __init__(self, state_value='17', district_value='0', block_value='0', panchayat_value='0', gs_date_value='0',
                 data_dir_path='C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/scrapy_spiders/post_requests_test'):
            super().__init__()
            self.state_value = state_value
            self.district_value = district_value
            self.block_value = block_value
            self.panchayat_value = panchayat_value
            self.gs_date_value = gs_date_value
            self.data_dir_path = data_dir_path


    def parse(self, response, **kwargs):
        form = generate_form(response, level='state', state_value=self.state_value)

        yield FormRequest.from_response(response, formdata=form, callback=self.parse_district)

    def parse_district(self, response):
        district_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/@value').getall()
        district_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/text()').getall()
        self.district_value = district_values_list[1]

        form = generate_form(response, level='district', state_value=self.state_value, district_value=self.district_value)
        yield FormRequest.from_response(response, formdata=form, callback=self.parse_block)


    def parse_block(self, response):
        block_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/@value').getall()
        block_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/text()').getall()
        self.block_value = block_values_list[1]

        form = generate_form(response, level='Block', state_value=self.state_value, district_value=self.district_value,
                                block_value=self.block_value)
        yield FormRequest.from_response(response, formdata=form, callback=self.parse_panchayat)

    def parse_panchayat(self, response):
        panchayat_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option/@value').getall()
        panchayat_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option/text()').getall()
        self.panchayat_value = panchayat_values_list[1]

        form = generate_form(response, level='Panchayat', state_value=self.state_value, district_value=self.district_value,
                                block_value=self.block_value, panchayat_value=self.panchayat_value)
        yield FormRequest.from_response(response, formdata=form, callback=self.parse_gs_date)


    def parse_gs_date(self, response):
        gs_date_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option/@value').getall()
        gs_date_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option/text()').getall()

        for gs_date_value in gs_date_values_list[1:]:
            self.gs_date_value = gs_date_value
            form = generate_form(response, level='GSDate', state_value=self.state_value, district_value=self.district_value,
                                 block_value=self.block_value, panchayat_value=self.panchayat_value, gs_date_value=self.gs_date_value)
            yield FormRequest.from_response(response, formdata=form, callback=self.parse_final)

    def parse_final(self, response):
        sa_start_date = response.xpath('//*[@id="ContentPlaceHolder1_lblSA_start_dt"]/text()').get()
        sa_end_date = response.xpath('//*[@id="ContentPlaceHolder1_lblSA_end_dt"]/text()').get()
        gs_date = response.xpath('//*[@id="ContentPlaceHolder1_lblGramSabha_dt"]/text()').get()
        public_hearing_date = response.xpath('//*[@id="ContentPlaceHolder1_lblPublic_Hearing_dt"]/text()').get()

        #Records Given for Social Audit
        sa_period_from_date = response.xpath('//*[@id="ContentPlaceHolder1_lblSA_Period_From_Date"]/text()').get()
        sa_period_to_date = response.xpath('//*[@id="ContentPlaceHolder1_lblSA_Period_To_Date"]/text()').get()
        wage_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblWage_exp"]/text()').get()
        mat_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblmat_exp"]/text()').get()
        total_exp = response.xpath('//*[@id="ContentPlaceHolder1_lbltotal_expen"]/text()').get()
        wage_given = response.xpath('//*[@id="ContentPlaceHolder1_lblwage_given"]/text()').get()
        mat_given = response.xpath('//*[@id="ContentPlaceHolder1_lblmat_given"]/text()').get()
        total_given = response.xpath('//*[@id="ContentPlaceHolder1_lbltotal_record_given"]/text()').get()

        # Social Audit Verification Information
        total_works = response.xpath('//*[@id="ContentPlaceHolder1_lbltot_work"]/text()').get()
        total_hh = response.xpath('//*[@id="ContentPlaceHolder1_lbltot_hh"]/text()').get()
        total_works_ver = response.xpath('//*[@id="ContentPlaceHolder1_lbltot_work_verified"]/text()').get()
        total_hh_ver = response.xpath('//*[@id="ContentPlaceHolder1_lbltot_hh_verified"]/text()').get()

        # Social Audit Grama Sabha
        gs_part = response.xpath('//*[@id="ContentPlaceHolder1_lblno_of_ppl_participated_gs"]/text()').get()

        total_sa_exp = response.xpath('//*[@id="ContentPlaceHolder1_lbltotal_expense"]/text()').get()

        # Qualitative Report
        qual_report = response.xpath('//*[@id="ContentPlaceHolder1_lblqualitative_report"]/text()').get()

        yield {
            'state_id': self.state_value,
            'district_id': self.district_value,
            'block_id': self.block_value,
            'panchayat_id': self.panchayat_value,
            'gs_date_value': self.gs_date_value,
            'sa_start_date': sa_start_date,
            'sa_end_date': sa_end_date,
            'gs_date': gs_date,
            'public_hearing_date': public_hearing_date,
            'sa_period_from_date': sa_period_from_date,
            'sa_period_to_date': sa_period_to_date,
            'wage_exp': wage_exp,
            'mat_exp': mat_exp,
            'total_exp': total_exp,
            'wage_given': wage_given,
            'mat_given': mat_given,
            'total_given': total_given,
            'total_works': total_works,
            'total_hh': total_hh,
            'total_works_ver': total_works_ver,
            'total_hh_ver': total_hh_ver,
            'gs_part': gs_part,
            'total_sa_exp': total_sa_exp,
            'qual_report': qual_report
        }


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(AspxSpider)
    process.start() # the script will block here until the crawling is finished


# for shell
# scrapy shell "https://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng"
# from scrapy import FormRequest, Request
# r = FormRequest.from_response(response, formdata=form)
# fetch(r)
# view(response)
