from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import datetime

ticker = "EQNR"

url_scrape = "https://finance.yahoo.com/quote/" + ticker + ".OL?p=" + ticker + ".OL&.tsrc=fin-srch"
#url_scrape = "https://finance.yahoo.com/quote/SSO.OL?p=SSO.OL&.tsrc=fin-srch"

# open webpage
client = urlopen(url_scrape)

# read page
raw_html = client.read()

# close webpage
client.close()

page_soup = soup(raw_html, "html.parser")
title = page_soup.find("title")
#Equinor ASA (EQNR) Stock Price, Quote, History & News - Yahoo Finance
print(title.text)

instrument_current_price = page_soup.find("span", {"data-reactid": "14"}).text

instrument_current_price_change = page_soup.find("span", {"data-reactid": "16"}).text



instrument_previous_close = page_soup.find("td", {"data-test": "PREV_CLOSE-value"}).find("span").text

instrument_price_open = page_soup.find("td", {"data-test": "OPEN-value"}).find("span").text
date = datetime.datetime.now().date()


out_filename = "../scraped_data/" + str(date) + "_" + ticker + ".csv"

# norsk csv bruker ; som verdiskille og "," som komma
headers = "stock_name;price;price_change \n"

f = open(out_filename, "w")
f.write(headers)

f.write(ticker + ";" + instrument_current_price + ";" + instrument_current_price_change + "\n")


f.close()
def lol():


    for index, element in enumerate(elements):
        instrument_name = element.find("span", {"class": "Typography__StyledTypography-sc-10mju41-0 dmJcIB"})

        # includes %: instrument_change = element.find_all("td", {"class": "Td__StyledTd-sc-1r6yxrk-0 eSYZap"})
        instrument_change = element.find("span", {"class": "Development__StyledDevelopment-hnn1ri-0"})

        instrument_price = element.find("td",
                                        {"class": "Td__StyledTd-sc-1r6yxrk-0 eSYZap Media__StyledDiv-sc-1dic02p-0 fxoRoi"})

        # instrument_change_negative = element.find("span", {"class": "Development__StyledDevelopment-hnn1ri-0 cuAsQS"})
        # Positive: Development__StyledDevelopment-hnn1ri-0 kokOki
        # Negative: Development__StyledDevelopment-hnn1ri-0 cuAsQS
        if instrument_name is not None:
            instrument_name = instrument_name.text
            instrument_change = instrument_change["value"].replace(".", ",")
            instrument_price = instrument_price.text
            # print(instrument_name, instrument_change + '%', instrument_price)
            print(index, instrument_name, instrument_change, instrument_price)
            f.write(str(index) + ";" + instrument_name + ";" + instrument_change + ";" + instrument_price + "\n")

    f.close()
