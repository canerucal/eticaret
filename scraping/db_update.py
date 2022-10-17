import psycopg2

connection = psycopg2.connect(
    user = "btbecirgkryyve",
    password = "23bebea366f5c8b8ce063c9b68d987a321bb979dee22aad3d975f7398dd4e652",
    host = "ec2-23-20-140-229.compute-1.amazonaws.com",
    port = "5432",
    database = "d7i1hcukm4nttn"
)

deneme = '3'

cursor = connection.cursor()
insert_query = """SELECT url FROM brand where url = '/apple/macbook-pro-m1-max-10c-cpu-32c-gpu-64gb-1-tb-ssd-macos-16-qhd-uzay-grisi-p-318500226'"""
cursor.execute(insert_query)
records = cursor.fetchall()
print(records)

cursor.close()
connection.close()