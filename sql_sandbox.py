import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='forPythonuse//', database='evaluations')
mycursor = mydb.cursor()

mycursor.execute("SELECT title, score FROM movies_evaluations")

for row in mycursor:
    row = str(row)
    print(row)
    print(type(row))
