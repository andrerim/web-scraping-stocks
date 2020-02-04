from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import datetime


#NO LONGER WORKS
my_url = "https://www.nordnet.no/market/no"

# open webpage
client = urlopen(my_url)

# read page
raw_html = client.read()

# close webpage
client.close()

page_soup = soup(raw_html, "html.parser")
tabels = page_soup.find_all("div", {"class": "InstrumentsPanel__Padded-hx9m9d-1 elYBrb"})
most_traded = tabels[0]

elements = most_traded.find_all("tr", {"class": "Tr__StyledTr-sc-1aap6l7-0 kdcphJ"})
date = datetime.datetime.now().date()
out_filename = str(date) + "_stock_prices_most_traded.csv"
# norsk csv bruker ; som verdiskille og "," som komma
headers = "rank;stock_name;change;price \n"

f = open(out_filename, "w")
f.write(headers)

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
