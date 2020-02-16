from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import os


def scrape_historical_data(ticker):
    print("Fetching data on", ticker)
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
    # find instrument name
    instr_name_pos_start = title.find("(") + 1
    instr_name_pos_end = title.find(".OL")
    instr_name = title[instr_name_pos_start:instr_name_pos_end]


    table_head = page_soup.find("thead")
    table_headers = ""
    for row in table_head:
        for cols in row:
            table_headers += cols.text + ";"

    dir_path = "../scraped_data"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    out_filename = "../scraped_data/historical_data_" + instr_name + ".csv"

    with open(out_filename, "w") as f:
        f.write(table_headers + "\n")

        table_body = page_soup.find("tbody")

        for tab in table_body:
            data = ""
            for span in tab:
                data += span.text + ";"
            f.write(data + "\n")

    return instr_name


