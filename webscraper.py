import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv


# opening up connection, grabbing the page
my_url = "https://www.vuokraovi.com/vuokra-asunnot"
uClient = uReq(my_url)
page_html = uClient.read()
page_soup = soup(page_html, "html.parser")


filename = "asunnot.csv"
f = open(filename, "w")

headers = "Kohdetta Vuokraa, Huoneistot, Talotyyppi ja Koko, Sijainti, Vapautuu, Vuokra, \n"

f.write(headers)
count = 0
# grabs the lists for headers
pages = soup(page_html, "html.parser").findAll("ul", {"class":"pagination"})

lastpage = int(pages[0].findAll("li")[7].text)

pages = list(range(1, int(lastpage) + 1))
for page in pages:
	my_url = "https://www.vuokraovi.com/vuokra-asunnot?page=%s&pageType=" % (page)
	containers = page_soup.findAll("div", {"class": "list-item-container"})
	uClient = uReq(my_url)
	page_html = uClient.read()
	page_soup = soup(page_html, "html.parser")
	print("Processing page: %s" % (page))

	for container in containers:
		try:
			Vuokranantaja = container.findAll("div", {"class": "hidden-xs col-sm-3 col-4"})[0].img["alt"]
		except TypeError:
			Vuokranantaja = container.findAll("div", {"class": "hidden-xs col-sm-3 col-4"})[0].p.strong.text.strip()
		except:
			Vuokranantaja = "Vuokranantajat.fi"
		Huoneistot = container.findAll("li", {"class": "semi-bold"})[1].text

		Talotyyppi = container.findAll("li", {"class": "semi-bold"})[0].text

		Sijainti = \
		container.findAll("div", {"class": "hidden-xs col-sm-4 col-3"})[0].findAll("span", {"class": "address"})[
			0].text.strip().replace("\r", "").replace("\n", "").replace(" ", "").replace(",", ", ")
		try:
			Vapautuu = container.findAll("div", {"class": "hidden-xs col-sm-4 col-3"})[0].findAll("span", {
				"class": "showing-lease-container hidden-xs"})[0].li.text
		except AttributeError:
			Vapautuu = "Vuokranantaja N/A"
		Vuokra = container.findAll("li", {"class": "rent"})[0].text.strip()
		Vuokra = Vuokra.replace("\xa0", "").replace(" ", "")  #.split("€")[0]
		#kkpv = container.findAll("li", {"class": "rent"})[0].text.strip()
		#kkpv = kkpv.split(" ")[1]

		

		print("Kohdetta Vuokraa:", Vuokranantaja)
		print("Huoneistot:", Huoneistot)
		print("Talotyyppi ja Koko:", Talotyyppi)
		print("Sijainti:", Sijainti)
		print("Vapautuu:", Vapautuu)
		print("Vuokra:", Vuokra)
		print("")

		count += 1
		f.write(Vuokranantaja.replace(",", " |") + "," + Huoneistot.replace(",", " - ") + "," + Talotyyppi.replace(",",
																												   ".") + "," + Sijainti.replace(
			",", " -") + "," + Vapautuu + "," + Vuokra.replace(",", ".") + "\n")

f.close()
print("Asuntojen Määrä:", count)



# Browser

import io

seen = []
file = io.open("asunnot.csv", "r", encoding="ISO-8859-1")

def Haku(search):
    search = input("Kirjoita Hakusana:") + " "
    while True:
        line = file.readline()

        if search in line:
            if line not in seen:
                seen.append(line)
                print(line.replace(",", " | ").replace(" | ", "\n"))
            else:
                continue
        if len(line) == 0 and search not in line:
            print("Ei lisää tuloksia.")
            break
Haku(file)
file.close()
