from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

ticker = "EQNR"

url_scrape = "https://finance.yahoo.com/quote/" + ticker + ".OL/history?p=" + ticker + ".OL"

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
print(title)


table_head = page_soup.find("thead")
table_headers = ""
for row in table_head:
    for cols in row:
        table_headers += cols.text + ";"


out_filename = "../scraped_data/historical_data_" + ticker + ".csv"

f = open(out_filename, "w")
f.write(table_headers + "\n")

table_body = page_soup.find("tbody")

for tab in table_body:
    data = ""
    for span in tab:
        data += span.text + ";"
    f.write(data + "\n")

f.close()

