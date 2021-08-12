from scrapy import Request, FormRequest
import urllib

fetch('https://quotes.toscrape.com/login')

response.css('[name="csrf_token"]').getall()
response.css('[name="csrf_token"]').get()

response.css('[name="csrf_token"] ::attr(value)').get()

form = {
'csrf_token': response.css('[name="csrf_token"] ::attr(value)').get(),
'username': 'user',
'password': '1234'
}

# use this when sending requests from the same page
r = FormRequest.from_response(response, formdata=form)

fetch(r)

response.css('a:contains(Logout)')

r = Request(url='https://quotes.toscrape.com/login', headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
        body=urllib.parse.urlencode(form), method='POST')

urllib.parse.urlencode(form)
