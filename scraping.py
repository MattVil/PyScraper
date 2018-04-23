import urllib.parse
import urllib.request
import sys
from statistics import mean
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

URL = 'https://www.amazon.fr/s/ref=nb_sb_noss_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords='
NB_RESULT_SELECTED = 100

key_word = ""
for i in range(1, len(sys.argv)):
    key_word += sys.argv[i] + " "
print("Search \"{}\" on Amazon ...".format(key_word))

URL += key_word.replace(" ", "+")
# print(url)

prices = []
cmpt_page = 1

while(len(prices) < NB_RESULT_SELECTED):
    print("\tPAGE {}".format(cmpt_page))
    req = urllib.request.Request(URL)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    page = str(respData)

    soup_page = BeautifulSoup(page, 'html.parser')
    # spans = soup_page.find_all("span", class_="s-price")
    # print(spans.text)
    price_fields = []
    for span in soup_page.find_all("span", class_="s-price"):
        price_fields.append(span.text)


    for price in price_fields:
        price = price.replace("EUR ", "")
        price = price.replace(",", ".")
        try:
            prices.append(float(price))
        except ValueError:
            print("LOG : Oops! a string cannot be converted to float.")

    next_page = soup_page.find  ("a", id="pagnNextLink", class_="pagnNext")
    # print(next_page)
    URL = "https://www.amazon.fr" + next_page.get('href')
    # print("URL : \t"+URL)
    cmpt_page += 1
    print("Nb product : {}".format(len(prices)))

moyenne = mean(prices)

fig = plt.figure("distribution du prix de " + key_word + "sur amazon, prix moyen : " + str(round(moyenne, 2)) + "€")
plt.hist(prices, normed=1)
plt.show()
