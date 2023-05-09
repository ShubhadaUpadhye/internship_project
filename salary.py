import mysql.connector as con

mydb = con.connect(host='localhost', user='root', password='mysqlp@$$')
mycursor = mydb.cursor()

