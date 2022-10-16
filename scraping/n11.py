# n11
import requests
from bs4 import BeautifulSoup

main_url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
for a in range(1,6):
    url = main_url+'?ipg={}'.format(a)
    page = requests.get(url) #html request
    soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
    tags = soup.find("div", {'class':"catalogView"}).find_all('a')

    for tag in tags:
        tag = tag['href']
        # print('url:', tag)
        r = requests.get(tag)
        soup2 = BeautifulSoup(r.content, "html.parser")
        data = soup2.find('div', {'class': 'unf-prop-context'}).find('ul').find_all('p', {'class': 'unf-prop-list-title'})
        data = list(data)

        key_data = []
        for i in data:
            i = i.text
            key_data.append(i)

        value_data = []
        data2 = soup2.find('div', {'class': 'unf-prop-context'}).find('ul').find_all('p', {'class': 'unf-prop-list-prop'})
        data2 = list(data2)
        for k in data2:
            k = k.text
            value_data.append(k)


        dictionary = dict(zip(key_data, value_data))
        brand = dictionary['Marka']
        model_name = soup2.find('h1', {'class': 'proName'}).text
        model_name = " ".join(model_name.split())
        model_no = dictionary['Model']
        print(model_no.lower())
        os = dictionary['İşletim Sistemi']
        cpu = dictionary['İşlemci']
        cpu_gen = dictionary['İşlemci Modeli']
        ram = dictionary['Bellek Kapasitesi']
        disk_capacity = dictionary['Disk Kapasitesi']
        screen_size = dictionary['Ekran Boyutu']
        rating = soup2.find('strong', {'class': 'ratingScore r100'})
        # if rating is None:
        #     # print('None')
        # else:
        #     rating = rating.text
        #     # print(rating)
        price = soup2.find('div', {'class': 'unf-p-summary-price'}).text
        # print(price)