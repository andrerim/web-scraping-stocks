from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import datetime

ticker = "EQNR"

url_scrape = "https://finance.yahoo.com/quote/" + ticker + ".OL?p=" + ticker + ".OL&.tsrc=fin-srch"

# open webpage
client = urlopen(url_scrape)

# read page
raw_html = client.read()

# close webpage
client.close()

page_soup = soup(raw_html, "html.parser")
title = page_soup.find("title").text
#Equinor ASA (EQNR) Stock Price, Quote, History & News - Yahoo Finance
instr_name_pos = title.find("Stock Price")
instr_name = title[:instr_name_pos]

instr_curr_price = page_soup.find("span", {"data-reactid": "14"}).text

instr_curr_price_change = page_soup.find("span", {"data-reactid": "16"}).text
# +0.80 (+0.48%)
value_percent_position = instr_curr_price_change.find("(")

instr_curr_price_change_value = instr_curr_price_change[:value_percent_position-1]
instr_curr_price_change_percent = instr_curr_price_change[value_percent_position+1:len(instr_curr_price_change)-1]


instr_prev_close = page_soup.find("td", {"data-test": "PREV_CLOSE-value"}).find("span").text

instr_price_open = page_soup.find("td", {"data-test": "OPEN-value"}).find("span").text



date = datetime.datetime.now().date()


out_filename = "../scraped_data/" + str(date) + "_" + ticker + ".csv"

# norsk csv bruker ; som verdiskille og "," som komma
headers = "stock_name;price;price_change;price_change%;prev_close;open \n"

with open(out_filename, "w") as f:
    f.write(headers)
    f.write(instr_name + ";" + instr_curr_price + ";" + instr_curr_price_change_value + ";" + instr_curr_price_change_percent + ";" + instr_prev_close + ";" + instr_price_open + "\n")

