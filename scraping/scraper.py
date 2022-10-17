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
        print('Veri kazıma işlemine başlandı.')
        if a == 2:
            print("Kazıma işleminin %20'si tamamlandı")
            print("(X----)")
        elif a == 3:
            print("Kazıma işleminin %40'ı tamamlandı")
            print("(XX---)")
        elif a == 4:
            print("Kazıma işleminin %60'ı tamamlandı")
            print("(XXX--)")
        elif a == 5:
            print("Kazıma işleminin %80'i tamamlandı")
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
                        photo = item['src'][0: start:] + item['src'][end + 1::]
                        break

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
                global brand, model_name, model_no, price, point, website, os, cpu, cpu_gen, ram, ssd_size, hdd_size,screen_size
                brand, model_name, model_no, price, point, website, os, cpu, cpu_gen, ram, ssd_size, hdd_size,screen_size = "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok", "bilgi yok"
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
                        cpu_gen = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 232:
                        ram = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 249:
                        ssd_size = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 467:
                        hdd_size = list(list(i.values())[1].values())[0].lower()
                    elif attr_check == 23:
                        screen_size = list(list(i.values())[1].values())[0].lower()

                        duplicate_check = """select url from brand where url='"""+tag+"""'"""
                        cursor.execute(duplicate_check)
                        try:
                            global record
                            record = cursor.fetchall()[0][0]
                        except:
                            record = " "

                        point = str(point)
                        price = str(price)

                        if record == tag:
                            print('aynı kayıt olduğu için kaydedilmedi.', tag)
                            print('-------')
                            price_check = """SELECT price FROM site_info WHERE url = '"""+tag+"""'"""
                            point_check = """SELECT product_point FROM site_info WHERE url = '"""+tag+"""'"""
                            cursor.execute(price_check)
                            price_record = cursor.fetchall()[0][0]
                            cursor.execute(point_check)
                            point_record = cursor.fetchall()[0][0]

                            if price != price_record:
                                print('fiyat güncelleniyor!')
                                new_price = price
                                price_update = """UPDATE site_info SET price ='"""+new_price+"""' WHERE url = '"""+tag+"""'"""
                                cursor.execute(price_update)
                                connection.commit()
                            if point != point_record:
                                print('puan güncelleniyor')
                                new_point = point
                                point_update = """UPDATE site_info SET product_point ='"""+new_point+"""' WHERE url ='"""+tag+"""'"""
                                cursor.execute(point_update)
                                connection.commit()
                        else:
                            brand_insert = """INSERT INTO brand VALUES ('"""+tag+"""', '"""+brand+"""', '"""+model_name+"""', '"""+model_no+"""', '"""+photo+"""');"""
                            hardware_insert = """INSERT INTO hardware VALUES ('"""+tag+"""', '"""+os+"""', '"""+cpu+"""', '"""+cpu_gen+"""', '"""+ram+"""', '"""+ssd_size+"""', '"""+hdd_size+"""', '"""+screen_size+"""');"""
                            site_insert = """INSERT INTO site_info VALUES ('"""+tag+"""', '"""+point+"""', '"""+price+"""', '"""+website+"""');"""
                            cursor.execute(brand_insert)
                            cursor.execute(hardware_insert)
                            cursor.execute(site_insert)
                            connection.commit()
                            print(brand, 'pc kaydedildi.')
                            print('------')
        
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
            brand_n11 = dictionary['Marka']
            model_name_n11 = soup2.find('h1', {'class': 'proName'})
            if model_name_n11 is None:
                model_name_n11 = "Bilgi yok"
            else:
                model_name_n11 = model_name_n11.text
            model_name_n11 = " ".join(model_name_n11.split()).lower()
            model_no_n11 = dictionary['Model'].lower()
            os_n11 = dictionary['İşletim Sistemi'].lower()
            cpu_n11 = dictionary['İşlemci'].lower()
            cpu_gen_n11 = dictionary['İşlemci Modeli'].lower()
            ram_n11 = dictionary['Bellek Kapasitesi'].lower()
            disk_capacity_n11 = dictionary['Disk Kapasitesi'].lower()
            screen_size_n11 = dictionary['Ekran Boyutu'].lower()
            point_n11 = soup2.find('strong', {'class': 'ratingScore r100'})
            if point_n11 is None:
                point_n11 = "Bilgi yok"
            else:
                point_n11 = point_n11.text
            price_n11 = soup2.find('div', {'class': 'unf-p-summary-price'})
            if price_n11 is None:
                price_n11 = "Bilgi yok"
            else:
                price_n11 = price_n11.text
            website_n11 = 'n11'

            if brand_n11 is None:
                brand_n11 = "Bilgi yok"
            elif model_name_n11 is None:
                model_name_n11 = "Bilgi yok"
            elif model_no_n11 is None:
                model_no_n11 = "Bilgi yok"
            elif os_n11 is None:
                os_n11 = "Bilgi yok"
            elif cpu_n11 is None:
                cpu_n11 = "Bilgi yok"
            elif cpu_gen_n11 is None:
                cpu_gen_n11 = "Bilgi yok"
            elif ram_n11 is None:
                ram_n11 = "Bilgi yok"
            elif disk_capacity_n11 is None:
                disk_capacity_n11 = "Bilgi yok"
            elif screen_size_n11 is None:
                screen_size_n11 = "Bilgi yok"

            duplicate_check2 = """select url from brand where url='"""+tag+"""'"""
            cursor.execute(duplicate_check2)
            try:
                global record2
                record2 = cursor.fetchall()[0][0]
            except:
                record2 = " "

            if record2 == tag:
                print('aynı kayıt olduğu için kaydedilmedi.', tag)
                print('-------')
                price_check = """SELECT price FROM site_info WHERE url = '"""+tag+"""'"""
                point_check = """SELECT product_point FROM site_info WHERE url = '"""+tag+"""'"""
                cursor.execute(price_check)
                price_record = cursor.fetchall()[0][0]
                cursor.execute(point_check)
                point_record = cursor.fetchall()[0][0]

                if price_n11 != price_record:
                    print('fiyat güncelleniyor!')
                    new_price = price_n11
                    price_update = """UPDATE site_info SET price ='"""+new_price+"""' WHERE url = '"""+tag+"""'"""
                    cursor.execute(price_update)
                    connection.commit()
                if point_n11 != point_record:
                    print('puan güncelleniyor')
                    new_point = point_n11
                    point_update = """UPDATE site_info SET product_point ='"""+new_point+"""' WHERE url ='"""+tag+"""'"""
                    cursor.execute(point_update)
                    connection.commit()
            else:
                brand_insert2 = """INSERT INTO brand VALUES ('"""+tag+"""', '"""+brand_n11+"""', '"""+model_name_n11+"""', '"""+model_no_n11+"""');"""
                hardware_insert2 = """INSERT INTO hardware VALUES ('"""+tag+"""', '"""+os_n11+"""', '"""+cpu_n11+"""', '"""+cpu_gen_n11+"""', '"""+ram_n11+"""', '"""+disk_capacity_n11+"""', '"""+screen_size_n11+"""');"""
                site_insert2 = """INSERT INTO site_info VALUES ('"""+tag+"""', '"""+point_n11+"""', '"""+price_n11+"""', '"""+website_n11+"""');"""
                cursor.execute(brand_insert2)
                cursor.execute(hardware_insert2)
                cursor.execute(site_insert2)
                connection.commit()
                print(brand_n11, 'pc kaydedildi.')
                print('---------')

getTrendyolData()
print('Trendyol kazıma işlemi tamamlandı.')
getn11Data()
print('n11 kazıma işlemi tamamlandı.')
cursor.close()
connection.close()