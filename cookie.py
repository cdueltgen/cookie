import re
import requests
from pyquery import PyQuery
from bs4 import BeautifulSoup as BS

# This is how you use requests to get data
# WRONG you's think this would work, but it doesn't. See below for curl command
# r = requests.post("https://www.girlscouts.org/councilfinder/results.asp", data="Zip=94703")
# for i in r.iter_lines():
    # print i
# curl
# curl https://www.girlscouts.org/councilfinder/results.asp -d "Zip=94703"

# address = "https://www.girlscouts.org/councilfinder/results.asp"

# Using PyQuery
# html = open("cookie.html", 'r').read()
# jquery = PyQuery(html)

def requestHTML(zipcode):
    address = "https://www.girlscouts.org/councilfinder/results.asp"
    payload = {"Zip":zipcode}
    # data_args = "Zip=" + zipcode
    r = requests.post(address, data=payload)
    return r

def make_text(r):
    html = ""
    for i in r.iter_lines():
        html += i
    # print html
    return html

def get_test_file():
    r = open('data/test_cookie.html').read()
    return r

def soup_me(html):
    # Using BS to find "Girl Scouts of"
    # soup.find_all(text=re.compile("Girl Scouts of"))
    # But not all are "Girl Scouts of"
    # This finds all the ones that are bold, council is last one?
    soup = BS(html)
    b = soup.find_all('b')
    print b[-1].text

def main():
    test_zips = ['01060', '02199', '10557', '17765', '26717', '28072', '36908', '45740', '62524', '74438', '94703']
    for zc in test_zips:
        r = requestHTML(zc)
        html = make_text(r)
        soup_me(html)

main()