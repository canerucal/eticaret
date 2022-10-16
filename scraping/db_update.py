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
insert_query = """INSERT INTO BRAND VALUES ("""+deneme+""", 'Apple', 'Macbook Air', '54234523', '4fdsafda')"""
cursor.execute(insert_query)
connection.commit()
cursor.close()
connection.close()