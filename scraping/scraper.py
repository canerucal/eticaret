# n11
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
tags = soup.find("div", {'class':"catalogView"}).find_all('a')

for tag in tags:
    tag = tag['href']
    r = requests.get(tag)
    soup2 = BeautifulSoup(r.content, "html.parser")
    data = soup2.find('div', {'class': 'unf-prop-context'}).find('ul')
    print(data)

    # li=[x.get_text() for x in data.select('[class="unf-prop-context"] li')]
    # print(li)
    # liste = []
    # for li in data.find_all("li"):
    #     print(li.text)



# for i in range(0,1): #load more yapılması için 5 sayfa ilerlemek için for döngüsü yazıldı
#     #trendyol laptop sekmesinden url'lerin çekilmesi
#     url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
#     page = requests.get(url) #html request
#     soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
#     tags = soup.find("div", {'class':"catalogView"}).find_all('a') #ürün linklerinin alınması a taglerinin çekilmesi
#     i = 1
#     for tag in tags:
#         tag = tag['href']
#         r = requests.get(tag).text
#         print(r)
#         data = soup.find('ul', class_='unf-prop-list more-detail-animate')
#         print(data)