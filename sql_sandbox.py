import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='forPythonuse//', database='evaluations')
mycursor = mydb.cursor()








tuple = (1, 2, 3, 4, 5)


x = str(tuple[0])
print(x)

y = ''.join("{} | {} | {}".format(str(tuple[0]), str(tuple[1]), str(tuple[2])))
print(y)

