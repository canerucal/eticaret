import requests, re, json
from bs4 import BeautifulSoup

main_url = "https://www.trendyol.com/laptop-x-c103108"
for a in range(1,6):
    url = main_url+'?pi={}'.format(a)
    page = requests.get(url) #html request
    soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
    tags = soup.find("div", {'class':"prdct-cntnr-wrppr"}).find_all('a') #ürün linklerinin alınması a taglerinin çekilmesi


# https://cdn.dsmcdn.com/ty518/product/media/images/20220826/13/165993243/230886343/1/1_org_zoom.jpg
# https://cdn.dsmcdn.com/mnresize/128/192/ty518/product/media/images/20220826/13/165993243/230886343/1/1_org_zoom.jpg
    for tag in tags:
        tag = tag['href']
        r = requests.get('https://www.trendyol.com'+tag)
        soup2 = BeautifulSoup(r.content, "html.parser")
        # image = soup2.get.img('src', {'class': 'base-product-image'}).find('src')
        # print(image)
        for item in soup2.find_all('img'):
            if str(item).find('mnresize') > 0:
                item['src'] = item['src'].replace('/mnresize','')
                start = item['src'].index('com')+3
                end = item['src'].index('ty')-2
                if len(item['src'])>end:
                    item['src'] = item['src'][0: start:] + item['src'][end + 1::]
                    print('ürün görseli:',item['src'])

        r = r.text
        print('url:','https://www.trendyol.com'+tag)

        #trendyolda 2 farklı js regex ifadesi var. bu sebeple 2 match koşulu yazıldı.
        matches1 = re.search(r"window.__PRODUCT_DETAIL_APP_INITIAL_STATE__=({.*}});window", r)
        matches2 = re.search(r"window.__PRODUCT_DETAIL_APP_INITIAL_STATE__\s=\s({.*}})", r)

        if matches1 is not None:
            matches = matches1
        elif matches2 is not None:
            matches = matches2
        else:
            print('Lütfen regex ifadelerini veya json data kaynaklarını kontrol edin.')

        if matches is not None:
            json_data = json.loads(matches.group(1))
            print('Brand:', (json_data['product']['brand']['name']).lower()) #marka adı
            print('Model name:', (json_data['product']['name'].lower())) #model adı
            print('Model no:', (json_data['product']['productCode'].lower())) #model no
            print('Fiyat:', (json_data['product']['price']['discountedPrice']['value'])) #buradan fiyata git matches2 işlemeyi unutma
            print('Skor:', (json_data['product']['ratingScore']['averageRating'])) #buradan puana git
            print('Trendyol') #websitesi
            for i in json_data['product']['attributes']:
                attr_check = list(list(i.values())[0].values())[1]
                if attr_check == 28:
                    print('Os:', list(list(i.values())[1].values())[0])
                elif attr_check == 168:
                    print('CPU:', list(list(i.values())[1].values())[0])
                elif attr_check == 320:
                    print('İşlemci Nesli:', list(list(i.values())[1].values())[0])
                elif attr_check == 232:
                    print('RAM:', list(list(i.values())[1].values())[0])
                elif attr_check == 249:
                    print('SSD:', list(list(i.values())[1].values())[0])
                elif attr_check == 467:
                    print('HDD:', list(list(i.values())[1].values())[0])
                elif attr_check == 23:
                    print('Ekran Boyutu:', list(list(i.values())[1].values())[0])
            print('--------------------')



