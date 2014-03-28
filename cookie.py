import requests
from bs4 import BeautifulSoup as BS
from flask import Flask, request, render_template, flash, session

from councils_with_gf_cookies import councils
from zips import zips

app = Flask(__name__)
app.secret_key = "SHHHHHHHHHHHH"
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

# THIS FUNCTION NO LONGER NEEDED
def get_test_file():
    r = open('data/test_cookie.html').read()
    return r

def soup_me(html):
    # Scrape the data using BeautifulSoup
    # This finds all the ones that are bold, council is last one
    soup = BS(html)
    b = soup.find_all('b')
    return b[-1].text

# THIS FUNCTION NO LONGER NEEDED
def get_councils():
    councils_dict = {}
    f = open("data/councils_with_gf_cookies.txt")
    for line in f:
        councils_dict[line.strip()] = 1
    f.close()
    return councils_dict

def check_it_yo(zc):
    # Takes a zip code as input at returns true if zip is in
    # a council that has GF cookies
    # test_zips = ['56387', '01060', '02199', '10557', '17765', '26717', '28072', '36908', '45740', '62524', '74438', '94703']
    # councils = get_councils()
    # zc = raw_input("Gimme a zip code to test> ")
    r = requestHTML(zc)
    html = make_text(r)
    q_council = soup_me(html)
    if councils.get(q_council):
        return True
    else:
        return False

@app.route('/', methods=["POST", "GET"])
def find_cookies():
    error = None
    if request.method == 'POST':
        zc = request.form['zipcode']
        if not zips.get(zc):
            flash("%s is not a valid zipcode" % zc)
        else:
            r = requestHTML(zc)
            html = make_text(r)
            q_council = soup_me(html)
            if councils.get(q_council):
                flash("%s has Gluten Free cookies" % q_council)
                # return render_template("index.html")
            else:
                flash("%s does not have Gluten Free cookies" % q_council)
                # return render_template("index.html")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
