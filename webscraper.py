import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


my_url = "https://www.newegg.com/global/fi-en/Video-Cards-Video-Devices/Category/ID-38"

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"item-container"})

filename = "products.csv"
f = open(filename, "w")

headers = "brand, product_name, shipping\n"

f.write(headers)

for container in containers:
	brand = container.findAll("img", {"class":" lazy-img"})[1]["title"]
	
	title_container = container.findAll("a",{"class":"item-title"})
	product_name = title_container[0].text

	shipping_container = container.findAll("li", {"class":"price-ship"})
	shipping = shipping_container[0].text.strip()
	if shipping == "":
		shipping = "N/A"



	print("Brand:", brand)
	print("Product:", product_name)
	print("Shipping:", shipping)

	f.write(brand + "," + product_name.replace(",", "|") + "," + shipping + "\n")

f.close()