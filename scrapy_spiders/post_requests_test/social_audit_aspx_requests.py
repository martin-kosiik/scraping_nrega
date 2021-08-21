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
                    block_value='0'):
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
        'ctl00$ContentPlaceHolder1$ddlPanchayat': '0',
        'ctl00$ContentPlaceHolder1$ddlGSDate': '0',
        'ctl00$ContentPlaceHolder1$ddlselect': '0'
    }
    return form

form = generate_form(response, level='state', state_value='17')

district_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/@value').getall()
district_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddldistrict"]/option/text()').getall()

district_value = district_values_list[1]

form = generate_form(response, level='district', state_value='17', district_value=district_value)

block_values_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/@value').getall()
block_names_list = response.xpath('//*[@id="ContentPlaceHolder1_ddlBlock"]/option/text()').getall()
block_value = block_values_list[1]

form = generate_form(response, level='Block', state_value='17', district_value=district_value,
                        block_value=block_value)


# fff
