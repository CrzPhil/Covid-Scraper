from urllib.request import urlopen, Request
import re
from bs4 import BeautifulSoup

# Due to mod_security, or some other feature that blocks known spider/bot user agents,
# we set a known browser user agent (here Mozilla)

url = Request('https://www.worldometers.info/coronavirus/#countries', headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# All of the above returns us the pure HTML of the site.
# Now we need to use regex to extract the text. Better said, extract the juice.

# Get total Cases
total_cases_raw = soup.find('div', class_='maincounter-number')
total_cases_string = str(total_cases_raw)
total_cases = re.search(">(.+?) <", total_cases_string).group(1)

# Get total Deaths
total_deaths_raw = soup.find_all('div', class_='maincounter-number')
total_deaths_string = str(total_deaths_raw[1])
total_deaths = re.search(">(.+?)<", total_deaths_string).group(1)

# Get total Recoveries
total_recoveries_raw = soup.find_all('div', class_='maincounter-number')
total_recoveries_string = str(total_recoveries_raw[2])
total_recoveries = re.search(">(.+?)<", total_recoveries_string).group(1)

# Active/Closed Cases
active_raw = soup.find_all('div', class_='col-md-6')
active_string = str(active_raw[0])
active_cases = re.search("\"number-table-main\">(.+?)<", active_string).group(1)

closed_raw = soup.find_all('div', class_='col-md-6')
closed_string = str(closed_raw[1])
closed_cases = re.search("\"number-table-main\">(.+?)<", closed_string).group(1)

# Here begins the Front-end Messages etc.

print("-------------------------------------------------------")
print("[+] Covid-19 real-time data scraper")
print("Total Worldwide Cases: " + total_cases)
print("Total Worldwide Deaths: " + total_deaths)
print("Total Worldwide recoveries: " + total_recoveries)
print("Total Worldwide closed cases: " + closed_cases)
print("Current Worldwide active cases: " + active_cases)

# Data by Country
all_data = soup.findAll("tbody")
# all_data[0] = All Table data. Country and every column.
# all_data[1] = North America, Europe, Asia, South America, Africa, Oceania
# all_data[2] = All

# print(all_data[0])

x = re.findall("td>(.+?)</td>", str(all_data[0]))

# print(x)

country_names = re.findall("/\">(.+?)</a></td>", str(all_data[0]))

# print(country_names)

table = soup.find_all("table")
all_columns = re.findall("<td style=\"font-weight: bold; text-align:right\">(.+?)</td>", str(table))

total_deaths_column = re.findall("<td style=\"font-weight: bold; text-align:right;\">(.+?)</td>", str(table))

active_cases_column = re.findall("<td style=\"text-align:right;font-weight:bold;\">(.+?)</td>", str(table))

# print(country_names)


