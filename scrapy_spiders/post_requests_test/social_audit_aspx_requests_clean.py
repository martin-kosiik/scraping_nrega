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
    data_dir_path='C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/scrapy_spiders/post_requests_test/sa_scraped_data_ka.csv'
    custom_settings = {
            'FEED_URI': 'file://' + data_dir_path,
            'FEED_FORMAT': 'csv',
        #    'HTTPCACHE_ENABLED': True,
        #    'POSTSTATS_INTERVAL': 200
        }

    # def __init__(self, state_value='17', district_value='0', block_value='0', panchayat_value='0', gs_date_value='0',
    #              data_dir_path='C:/Users/marti/OneDrive/Plocha/research_projects/scraping_nrega/scrapy_spiders/post_requests_test'):
    #         super().__init__()
    #         self.state_value = state_value
    #         self.district_value = district_value
    #         self.block_value = block_value
    #         self.panchayat_value = panchayat_value
    #         self.gs_date_value = gs_date_value
    #         self.data_dir_path = data_dir_path


    def parse(self, response, **kwargs):
        form = generate_form(response, level='state', state_value='15')

        yield FormRequest.from_response(response, formdata=form, callback=self.parse_district)

    def parse_district(self, response):
        district_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/@value').getall()
        district_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/text()').getall()
        district_value = district_values_list[1]
        #self.district_value = district_values_list[1]
        state_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlstate"]/option[@selected="selected"]/@value').get()

        form = generate_form(response, level='district', state_value=state_value, district_value=district_value)
        yield FormRequest.from_response(response, formdata=form, callback=self.parse_block)


    def parse_block(self, response):
        block_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/@value').getall()
        block_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/text()').getall()
#        self.block_value = block_values_list[1]
        #block_value = block_values_list[1]
        state_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlstate"]/option[@selected="selected"]/@value').get()
        district_value = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option[@selected="selected"]/@value').get()

        for block_value in block_values_list[1:]:
            form = generate_form(response, level='Block', state_value=state_value, district_value=district_value,
                                 block_value=block_value)
            yield FormRequest.from_response(response, formdata=form, callback=self.parse_panchayat)


        #form = generate_form(response, level='Block', state_value=state_value, district_value=district_value,
        #                        block_value=block_value)
        #yield FormRequest.from_response(response, formdata=form, callback=self.parse_panchayat)

    def parse_panchayat(self, response):
        panchayat_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option/@value').getall()
        panchayat_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option/text()').getall()
        #panchayat_value = panchayat_values_list[1]
#        self.panchayat_value = panchayat_value
        state_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlstate"]/option[@selected="selected"]/@value').get()
        district_value = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option[@selected="selected"]/@value').get()
        block_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option[@selected="selected"]/@value').get()

        #form = generate_form(response, level='Panchayat', state_value=state_value, district_value=district_value,
        #                        block_value=block_value, panchayat_value=panchayat_value)
        #yield FormRequest.from_response(response, formdata=form, callback=self.parse_gs_date)

        for panchayat_value in panchayat_values_list[1:]:
            form = generate_form(response, level='Panchayat', state_value=state_value, district_value=district_value,
                                block_value=block_value, panchayat_value=panchayat_value)
            yield FormRequest.from_response(response, formdata=form, callback=self.parse_gs_date)


    def parse_gs_date(self, response):
        gs_date_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option/@value').getall()
        gs_date_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option/text()').getall()
        state_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlstate"]/option[@selected="selected"]/@value').get()
        district_value = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option[@selected="selected"]/@value').get()
        block_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option[@selected="selected"]/@value').get()
        panchayat_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option[@selected="selected"]/@value').get()


        for gs_date_value in gs_date_values_list[1:]:
            form = generate_form(response, level='GSDate', state_value=state_value, district_value=district_value,
                                 block_value=block_value, panchayat_value=panchayat_value, gs_date_value=gs_date_value)
            yield FormRequest.from_response(response, formdata=form, callback=self.parse_final)

    def parse_final(self, response):
        state_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlstate"]/option[@selected="selected"]/@value').get()
        district_value = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option[@selected="selected"]/@value').get()
        block_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option[@selected="selected"]/@value').get()
        panchayat_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option[@selected="selected"]/@value').get()
        gs_date_value = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option[@selected="selected"]/@value').get()


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

        # Summary Of Reported Issues
        fm_reported = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[2]/text()').get()
        fm_closed = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[3]/text()').get()
        fd_reported = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[4]/text()').get()
        fd_closed = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[5]/text()').get()
        pv_reported = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[6]/text()').get()
        pv_closed = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[7]/text()').get()
        griev_reported = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[8]/text()').get()
        griev_closed = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[9]/text()').get()
        total_issues_reported = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[10]/text()').get()
        total_issues_closed = response.xpath('//*[@id="ContentPlaceHolder1_divReportedIssue"]//tbody//td[11]/text()').get()

        # Summary Of Action Taken Report
        fm_amount = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[2]/text()').get()
        fm_amount_recovered = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[3]/text()').get()
        fd_amount = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[4]/text()').get()
        penalty_paid = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[5]/text()').get()
        firs_filled = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[6]/text()').get()
        employees_suspended = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[7]/text()').get()
        employees_terminated = response.xpath('//*[@id="ContentPlaceHolder1_divATR"]//tbody//td[8]/text()').get()


        # Gram Panchayat Checklist
        # Job Cards
        job_cards_with_people = response.xpath('//*[@id="ContentPlaceHolder1_Label1"]/text()').get()
        job_cards_updated = response.xpath('//*[@id="ContentPlaceHolder1_Label3"]/text()').get()
        job_cards_renewed = response.xpath('//*[@id="ContentPlaceHolder1_Label4"]/text()').get()
        # Work & Wages
        demand_process = response.xpath('//*[@id="ContentPlaceHolder1_Label2"]/text()').get()
        unmet_demand = response.xpath('//*[@id="ContentPlaceHolder1_Label29"]//text()').get()
        problems_getting_wages = response.xpath('//*[@id="ContentPlaceHolder1_Label30"]//text()').get()
        # MGNREGS Administration
        musterrolls_at_worksite_maintained =  response.xpath('//*[@id="ContentPlaceHolder1_Label5"]/text()').get()
        seven_registers_maintained =  response.xpath('//*[@id="ContentPlaceHolder1_Label17"]/text()').get()
        # Personnel & Training ContentPlaceHolder1_Label28
        mates_selected_by_gs =  response.xpath('//*[@id="ContentPlaceHolder1_Label22"]/text()').get()
        mates_trained =  response.xpath('//*[@id="ContentPlaceHolder1_trmates"]/text()').get()
        adeq_manpower =  response.xpath('//*[@id="ContentPlaceHolder1_Label24"]/text()').get()
        person_in_charge_of_nrega_panch = response.xpath('//*[@id="ContentPlaceHolder1_Label25"]/text()').get()
        person_in_charge_of_nrega_panch_trained = response.xpath('//*[@id="ContentPlaceHolder1_Label27"]/text()').get()
        tech_support = response.xpath('//*[@id="ContentPlaceHolder1_Label28"]/text()').get()


        yield {
            'state_id': state_value,
            'district_id': district_value,
            'block_id': block_value,
            'panchayat_id': panchayat_value,
            'gs_date_value': gs_date_value,
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
            'qual_report': qual_report,
            'fm_reported': fm_reported,
            'fm_closed': fm_closed,
            'fd_reported': fd_reported,
            'fd_closed': fd_closed,
            'pv_reported': pv_reported,
            'pv_closed': pv_closed,
            'griev_reported': griev_reported,
            'griev_closed': griev_closed,
            'total_issues_reported': total_issues_reported,
            'total_issues_closed': total_issues_closed,
            'fm_amount': fm_amount,
            'fm_amount_recovered': fm_amount_recovered,
            'fd_amount': fd_amount,
            'penalty_paid': penalty_paid,
            'firs_filled': firs_filled,
            'employees_suspended': employees_suspended,
            'employees_terminated': employees_terminated,
            'job_cards_with_people': job_cards_with_people,
            'job_cards_updated': job_cards_updated,
            'job_cards_renewed': job_cards_renewed,
            'demand_process': demand_process,
            'unmet_demand': unmet_demand,
            'problems_getting_wages': problems_getting_wages,
            'musterrolls_at_worksite_maintained': musterrolls_at_worksite_maintained,
            'seven_registers_maintained': seven_registers_maintained,
            'mates_selected_by_gs': mates_selected_by_gs,
            'mates_trained': mates_trained,
            'adeq_manpower': adeq_manpower,
            'person_in_charge_of_nrega_panch': person_in_charge_of_nrega_panch,
            'person_in_charge_of_nrega_panch_trained': person_in_charge_of_nrega_panch_trained,
            'tech_support': tech_support
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
