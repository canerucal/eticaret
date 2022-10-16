# hepsiburada
import requests
from bs4 import BeautifulSoup
import pandas as pd

main_url = 'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98'
for a in range(1,6): #load more yapılması için 5 sayfa ilerlemek için for döngüsü yazıldı
    #trendyol laptop sekmesinden url'lerin çekilmesi
    url = main_url+'?sayfa={}'.format(a)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
    tags = soup.find("ul", {'class':"productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"}).find_all('a') #ürün linklerinin alınması a taglerinin çekilmesi
    for tag in tags:
        tag = tag['href']
        ad_check = str(tag)
        # print('url:', 'https://www.hepsiburada.com'+tag)
        if ad_check[0]!='/':
            try:
                r = requests.get('tag', headers=headers)
            except:
                print("bu bir reklamdır ve yönlendirme sebebiyle table tag'i gelmemektedir.")
        else:
            r = requests.get('https://www.hepsiburada.com'+tag, headers=headers)
            soup2 = BeautifulSoup(r.content, "html.parser")
            rating = soup2.find('span', {'class': 'rating-star'})
            price = soup2.find('span', {'data-bind': "markupText:'currentPriceBeforePoint'"})
            if rating is None:
                print('reklam yönlendirme yaptığı için duplicate kayda sebep oluyor. bu sebeple atlandı.')
            else:
                rating = rating.text
                price = price.text
                print(rating)
                print(price)
                print('hepsiburada')
            df = pd.read_html(r.content)
            print(df[4])