import urllib
import scrapy
from scrapy import FormRequest, Request
#import scraper_helper as sh
from scrapy.shell import inspect_response


class AspxSpider(scrapy.Spider):
    name = 'aspx'
    start_urls = ['https://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng']

    def parse(self, response, **kwargs):
        __VIEWSTATE = response.xpath('//*[@name="__VIEWSTATE"]/@value').get()
        __EVENTTARGET = response.xpath('//*[@name="__EVENTTARGET"]/@value').get()
        __EVENTARGUMENT = response.xpath('//*[@name="__EVENTARGUMENT"]/@value').get()
        __VIEWSTATEENCRYPTED = response.xpath('//*[@name="__VIEWSTATEENCRYPTED"]/@value').get()
        __VIEWSTATEGENERATOR = response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').get()
        __SCROLLPOSITIONX = response.xpath('//*[@name="__SCROLLPOSITIONX"]/@value').get()
        __SCROLLPOSITIONY = response.xpath('//*[@name="__SCROLLPOSITIONY"]/@value').get()
        __EVENTVALIDATION = response.xpath('//*[@name="__EVENTVALIDATION"]/@value').get()

        __SCROLLPOSITIONX = '0'
        __SCROLLPOSITIONY = '0'
        __EVENTTARGET = 'ctl00$ContentPlaceHolder1$ddlstate'
    #    __RequestVerificationToken = response.xpath('//*[@name="__RequestVerificationToken"]/@value').get()
    #    __dnnVariable = response.xpath('//*[@name="__dnnVariable"]/@value').get()
        form = {
            'ctl00$ScriptManager1': 'ctl00$UpdatePanel1|ctl00$ContentPlaceHolder1$ddlstate',
            '__LASTFOCUS': '',
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTTARGET': __EVENTTARGET if __EVENTTARGET else '',
            '__EVENTARGUMENT': __EVENTARGUMENT if __EVENTARGUMENT else '',
            '__VIEWSTATEENCRYPTED': __VIEWSTATEENCRYPTED,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            '__SCROLLPOSITIONX': __SCROLLPOSITIONX,
            '__SCROLLPOSITIONY': __SCROLLPOSITIONY,
            '__ASYNCPOST': 'true',
        #    '__RequestVerificationToken': __RequestVerificationToken,
        #    '__dnnVariable': __dnnVariable,
            'ctl00$ContentPlaceHolder1$ddlstate': 17,  # MADHYA PRADESH
            'ctl00$ContentPlaceHolder1$ddldistrict': 0,
            'ctl00$ContentPlaceHolder1$ddlBlock': 0,
            'ctl00$ContentPlaceHolder1$ddlPanchayat': 0,
            'ctl00$ContentPlaceHolder1$ddlGSDate': 0,
            'ctl00$ContentPlaceHolder1$ddlselect': 0
        }

        form = {
            'ctl00$ScriptManager1': 'ctl00$UpdatePanel1|ctl00$ContentPlaceHolder1$ddlstate',
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
            'ctl00$ContentPlaceHolder1$ddlstate': '17',  # MADHYA PRADESH
            'ctl00$ContentPlaceHolder1$ddldistrict': '0',
            'ctl00$ContentPlaceHolder1$ddlBlock': '0',
            'ctl00$ContentPlaceHolder1$ddlPanchayat': '0',
            'ctl00$ContentPlaceHolder1$ddlGSDate': '0',
            'ctl00$ContentPlaceHolder1$ddlselect': '0'
        }


        yield FormRequest('https://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng',
                          formdata=form,
                          callback=self.parse_table)

    def parse_table(self, response):
        rows = response.xpath('//table[contains(@id, "gvDetailsSearchView")]//tr[td]')
        for row in rows:
            yield {
                'code': row.xpath('./td[1]/text()').get(),
                'value': row.xpath('./td[2]/text()').get()
            }


# for shell
# scrapy shell "https://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng"
# from scrapy import FormRequest, Request
# r = FormRequest.from_response(response, formdata=form)
# fetch(r)
# view(response)


response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]').getall()
response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option').getall()
district_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/@value').getall()
district_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/text()').getall()


# we do need new __VIEWSTATE etc.

        __VIEWSTATE = response.xpath('//*[@name="__VIEWSTATE"]/@value').get()
        __EVENTTARGET = response.xpath('//*[@name="__EVENTTARGET"]/@value').get()
        __EVENTARGUMENT = response.xpath('//*[@name="__EVENTARGUMENT"]/@value').get()
        __VIEWSTATEENCRYPTED = response.xpath('//*[@name="__VIEWSTATEENCRYPTED"]/@value').get()
        __VIEWSTATEGENERATOR = response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').get()
        __EVENTVALIDATION = response.xpath('//*[@name="__EVENTVALIDATION"]/@value').get()

        __SCROLLPOSITIONX = '0'
        __SCROLLPOSITIONY = '0'
        __EVENTTARGET = 'ctl00$ContentPlaceHolder1$ddldistrict'

district_value = district_values_list[1]

    form = {
        'ctl00$ScriptManager1': 'ctl00$UpdatePanel1|ctl00$ContentPlaceHolder1$ddldistrict',
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
        'ctl00$ContentPlaceHolder1$ddlstate': '17',  # MADHYA PRADESH
        'ctl00$ContentPlaceHolder1$ddldistrict': district_value,
        'ctl00$ContentPlaceHolder1$ddlBlock': '0',
        'ctl00$ContentPlaceHolder1$ddlPanchayat': '0',
        'ctl00$ContentPlaceHolder1$ddlGSDate': '0',
        'ctl00$ContentPlaceHolder1$ddlselect': '0'
    }




block_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/@value').getall()
block_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/text()').getall()
block_value = block_values_list[1]

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

form = generate_form(response, level='state', state_value='17')
r = FormRequest.from_response(response, formdata=form)
fetch(r)
district_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/@value').getall()
district_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/text()').getall()

district_value = district_values_list[1]

form = generate_form(response, level='district', state_value='17', district_value=district_value)
r = FormRequest.from_response(response, formdata=form)
fetch(r)
block_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/@value').getall()
block_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/text()').getall()
block_value = block_values_list[1]

form = generate_form(response, level='Block', state_value='17', district_value=district_value,
                        block_value=block_value)
r = FormRequest.from_response(response, formdata=form)
fetch(r)
panchayat_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option/@value').getall()
panchayat_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlPanchayat"]/option/text()').getall()
panchayat_value = panchayat_values_list[1]

form = generate_form(response, level='Panchayat', state_value='17', district_value=district_value,
                        block_value=block_value, panchayat_value=panchayat_value)
r = FormRequest.from_response(response, formdata=form)
fetch(r)
gs_date_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option/@value').getall()
gs_date_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlGSDate"]/option/text()').getall()
gs_date_value = gs_date_values_list[1]

form = generate_form(response, level='GSDate', state_value='17', district_value=district_value,
                        block_value=block_value, panchayat_value=panchayat_value, gs_date_value=gs_date_value)
r = FormRequest.from_response(response, formdata=form)
fetch(r)

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

# Expenses for the facilitation of this Social Audit
printing_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblprinting_expense"]/text()').get()
video_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblvideography_expense"]/text()').get()
tea_exp = response.xpath('//*[@id="ContentPlaceHolder1_lbltea_expense"]/text()').get()
vrp_training_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblvrp_training_expense"]/text()').get()
vrp_travel_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblvrp_travel_expense"]/text()').get()
photo_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblphotocopying_expense"]/text()').get()
other_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblother_expense"]/text()').get()
vrp_honor_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblvrp_honorium_expense"]/text()').get()
stationary_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblstationary_expense"]/text()').get()
publicity_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblpublicity_expense"]/text()').get()
mic_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblmic_expense"]/text()').get()
photography_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblphotography_expense"]/text()').get()
shamiana_exp = response.xpath('//*[@id="ContentPlaceHolder1_lblshamiana_expense"]/text()').get()
total_sa_exp = response.xpath('//*[@id="ContentPlaceHolder1_lbltotal_expense"]/text()').get()

# Qualitative Report
qual_report = response.xpath('//*[@id="ContentPlaceHolder1_lblqualitative_report"]/text()').get()

# Gram Panchayat Checklist
# Job Cards


output_vals = {
'state_id': '17',
'district_id': district_value,
'block_id': block_value,
'panchayat_id': panchayat_value,
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


#
