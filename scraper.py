from urllib.request import urlopen, Request
import re
from bs4 import BeautifulSoup

# Due to mod_security, or some other feature that blocks known spider/bot user agents,
# we set a known browser user agent (here Mozilla)

url = Request('https://www.worldometers.info/coronavirus/#countries', headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# All of the above returns us the pure HTML of the site


class Country:
    def __init__(self, name, tot_cases, tot_rec, serious, tot_per_mil, death_per_mil, tot_tests, test_per_mil):
        self.name = name
        self.tot_cases = tot_cases
        self.tot_rec = tot_rec
        self.serious = serious
        self.tot_per_mil = tot_per_mil
        self.death_per_mil = death_per_mil
        self.tot_tests = tot_tests
        self.test_per_mil = test_per_mil


# Now we need to use regex to extract the text

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
# all_data[0] = All Table data; Country and every column
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

# print("Countries: ")
# print(len(country_names))

'''control = 0
for country in country_names:
    print("Stats for " + country + ": ")
    for i in range(8):
        if i == 0:
            print("Total Cases: " + all_columns[control])
            control += 1
        elif i == 1:
            print("Total Recovered: " + all_columns[control])
            control += 1
        elif i == 2:
            print("Serious or Critical: " + all_columns[control])
            control += 1
        elif i == 3:
            print("Total Cases/1M pop: " + all_columns[control])
            control += 1
        elif i == 4:
            print("Deaths/1M pop: " + all_columns[control])
            control += 1
        elif i == 5:
            print("Total Tests: " + all_columns[control])
            control += 1
        elif i == 6:
            print("Tests/1M pop: " + all_columns[control])
            control += 1
        elif i == 7:
            print("\n")
            control += 1'''

# Create Country List
countries = [Country(None, None, None, None, None, None, None, None) for i in range(len(country_names))]

# Add the data

control = 0
for i in range(len(country_names)):
    countries[i].name = country_names[i]
    for j in range(8):
        if j == 0:
            countries[i].tot_cases = all_columns[control]
            control += 1
        elif j == 1:
            countries[i].tot_rec = all_columns[control]
            control += 1
        elif j == 2:
            countries[i].serious = all_columns[control]
            control += 1
        elif j == 3:
            countries[i].tot_per_mil = all_columns[control]
            control += 1
        elif j == 4:
            countries[i].death_per_mil = all_columns[control]
            control += 1
        elif j == 5:
            countries[i].tot_tests = all_columns[control]
            control += 1
        elif j == 6:
            countries[i].test_per_mil = all_columns[control]
            control += 1
        elif j == 7:
            control += 1


for i in range(len(country_names)):
    print(countries[i].name + " data: ")
    print("Total Cases: " + countries[i].tot_cases)
    print("Total Recoveries: " + countries[i].tot_rec)
    print("Total serious/critical cases: " + countries[i].serious)
    print("Total Cases per Million: " + countries[i].tot_per_mil)
    print("Total Deaths per Million: " + countries[i].death_per_mil)
    print("Total Tests: " + countries[i].tot_tests)
    print("Total Tests per Million: " + countries[i].test_per_mil)
    print("\n")

# Problems:
# 1. Something with China is being very weird (doesn't seem to offset the data though)
# 2. Number 195, Diamond Princess is in italics and offsets the last few country names as it isn't parsed
