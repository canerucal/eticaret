import requests, re, json
from bs4 import BeautifulSoup
import psycopg2

def dbConn():
    global connection, cursor
    connection = psycopg2.connect(
        user = "btbecirgkryyve",
        password = "23bebea366f5c8b8ce063c9b68d987a321bb979dee22aad3d975f7398dd4e652",
        host = "ec2-23-20-140-229.compute-1.amazonaws.com",
        port = "5432",
        database = "d7i1hcukm4nttn"
    )
    cursor = connection.cursor()


def getTrendyolData():
    dbConn()
    main_url = "https://www.trendyol.com/laptop-x-c103108"
    for a in range(1,6):
        print('Veri kazıma işlemi başladı.')
        if a == 2:
            print("Kazıma işinin %20'si tamamlandı")
            print("(X----)")
        elif a == 3:
            print("Kazıma işinin %40'ı tamamlandı")
            print("(XX---)")
        elif a == 4:
            print("Kazıma işinin %60'ı tamamlandı")
            print("(XXX--)")
        elif a == 5:
            print("Kazıma işinin %80'i tamamlandı")
            print("(XXXX-)")
        
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
            for item in soup2.find_all('img'):
                if str(item).find('mnresize') > 0:
                    item['src'] = item['src'].replace('/mnresize','')
                    start = item['src'].index('com')+3
                    end = item['src'].index('ty')-2
                    if len(item['src'])>end:
                        item['src'] = item['src'][0: start:] + item['src'][end + 1::]

            r = r.text

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
                global brand, model_name, model_no, price, point, website, os, cpu, cpu_type, ram, ssd_size, hdd_size,screen_size, product_id
                brand = (json_data['product']['brand']['name']).lower() #marka adı
                model_name = (json_data['product']['name'].lower()) #model adı
                model_no = (json_data['product']['productCode'].lower()) #model no
                price =  (json_data['product']['price']['discountedPrice']['value']) #buradan fiyata git matches2 işlemeyi unutma
                point =  (json_data['product']['ratingScore']['averageRating']) #buradan puana git
                website = 'trendyol'
                for i in json_data['product']['attributes']:
                    attr_check = list(list(i.values())[0].values())[1]
                    if attr_check == 28:
                        os = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 168:
                        cpu = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 320:
                        cpu_type = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 232:
                        ram = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 249:
                        ssd_size = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 467:
                        hdd_size = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 23:
                        screen_size = list(list(i.values())[1].values())[0].lower()
                        
                        product_id = brand+"-"+cpu+"-"+os+"-"+ram+"-"+model_no+"-"+website
                        print(brand, cpu, os, ram, website)
                        insert_query = """INSERT INTO brand VALUES ('"""+product_id+"""', '"""+brand+"""', '"""+model_name+"""', '"""+model_no+"""')"""
                        cursor.execute(insert_query)
                        connection.commit()
                        print(brand, ' pc kaydedildi.')
        
def getn11Data():
    dbConn()
    main_url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar"
    for a in range(1,6):
        url = main_url+'?ipg={}'.format(a)
        page = requests.get(url) #html request
        soup = BeautifulSoup(page.content, "html.parser") #sayfa içeriğinin parse edilmesi
        tags = soup.find("div", {'class':"catalogView"}).find_all('a')

        for tag in tags:
            tag = tag['href']
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
    connection.commit()
    cursor.close()
    connection.close()

getTrendyolData()
cursor.close()
connection.close()