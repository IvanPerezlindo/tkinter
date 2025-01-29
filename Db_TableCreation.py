import psycopg2

con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432") #conexion to database

print("Database opened successfully")

#Create table on DB
cur = con.cursor() #The cursor allows you to capture a query and process each individual row at a time.
cur.execute('''CREATE TABLE motos
            (Marca CHAR(255),
            Modelo CHAR(255),
            Year INT);''') #we use the cursor method to create the table
print('Tabla cargada correctamente!')

con.commit() #apply changes to DB
con.close() #close conexion to DB

#to add a column to a table already created use ALTER TABLE