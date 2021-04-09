from urllib.request import urlopen, Request
import re
from bs4 import BeautifulSoup
import sys

# Due to mod_security, or some other feature that blocks known spider/bot user agents,
# we set a known browser user agent (here Mozilla)

url = Request('https://www.worldometers.info/coronavirus/#countries', headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# All of the above returns us the pure HTML of the site


class Country:
    def __init__(self, name, tot_cases, new_cases, tot_deaths, new_deaths, tot_rec, active_cases, serious, tot_per_mil,
                 death_per_mil, tot_tests, test_per_mil):
        self.name = name
        self.tot_cases = tot_cases
        self.new_cases = new_cases
        self.tot_deaths = tot_deaths
        self.new_deaths = new_deaths
        self.tot_rec = tot_rec
        self.active_cases = active_cases
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

# Find and parse table
table = soup.find("tbody")
all_data = []
for row in table.findAll("tr"):
    cells = row.findAll("td")
    # Strip/Cleanup the entries
    cells = [ele.text.strip() for ele in cells]
    # print(cells)
    all_data.append(cells)

# each sub-array of cells returns the following, which might come in usefully when visualising data:
# ['num_in_list', 'name', 'tot_cases', 'new_cases', 'tot_deaths', 'new_deaths', 'tot_recovered', 'some_number',
# 'active_cases', 'serious_cases', 'tot_per_mil', 'death_per_mil', 'tot_tests', 'tests_per_mil', 'population',
# 'continent', 'some_number', 'some_number', 'some_number']

# Since the first 8 entries of the 'cells' array are continents, we skip them here
countries_new = [Country(None, None, None, None, None, None, None, None, None, None, None, None)
                 for i in range(len(all_data)-8)]

# Add the data
# Control starts at 8 since the first 8 values sub-arrays are data of continents
control = 8
for i in range(len(countries_new)):
    for j in range(14):
        if j == 1:
            countries_new[i].name = all_data[control][j]
        elif j == 2:
            countries_new[i].tot_cases = all_data[control][j]
        elif j == 3:
            countries_new[i].new_cases = all_data[control][j]
        elif j == 4:
            countries_new[i].tot_deaths = all_data[control][j]
        elif j == 5:
            countries_new[i].new_deaths = all_data[control][j]
        elif j == 6:
            countries_new[i].tot_rec = all_data[control][j]
        # There is a weird value which isn't visible in the table so we skip it as it's unknown
        elif j == 7:
            pass
        elif j == 8:
            countries_new[i].active_cases = all_data[control][j]
        elif j == 9:
            countries_new[i].serious = all_data[control][j]
        elif j == 10:
            countries_new[i].tot_per_mil = all_data[control][j]
        elif j == 11:
            countries_new[i].death_per_mil = all_data[control][j]
        elif j == 12:
            countries_new[i].tot_tests = all_data[control][j]
        elif j == 13:
            countries_new[i].test_per_mil = all_data[control][j]

    # Increment control to point to next sub-array
    control += 1

if __name__ == "__main__":
    # Here begins the Front-end Messages etc.
    print("-------------------------------------------------------")
    print("[+] Covid-19 real-time data scraper")
    print("Total Worldwide Cases: " + total_cases)
    print("Total Worldwide Deaths: " + total_deaths)
    print("Total Worldwide recoveries: " + total_recoveries)
    print("Total Worldwide closed cases: " + closed_cases)
    print("Current Worldwide active cases: " + active_cases)
    print("\n")
    print("Just type the name of the country you want more data about below.")
    print("Type exit to leave the program.")
    print("\n")

    running = True

    while running:
        query = input("Country Name: ")

        if query == "exit":
            running = False
        else:
            for country in countries_new:
                if query == country.name:
                    print("Total Cases: " + country.tot_cases)
                    print("New Cases: " + country.new_cases)
                    print("Total Deaths: " + country.tot_deaths)
                    print("New Deaths: " + country.new_deaths)
                    print("Total Recoveries: " + country.tot_rec)
                    print("Active Cases: " + country.active_cases)
                    print("Total serious/critical cases: " + country.serious)
                    print("Total Cases per Million: " + country.tot_per_mil)
                    print("Total Deaths per Million: " + country.death_per_mil)
                    print("Total Tests: " + country.tot_tests)
                    print("Total Tests per Million: " + country.test_per_mil)
                    print("\n")
                    break
                elif country.name == countries_new[len(countries_new)-1].name and\
                        countries_new[len(countries_new)-1].name != query:
                    print("The name you typed returned no matches in the database.")
                    print("\n")
