import mysql.connector

password = input('Enter password for "evaluations" database:\n')
mydb = mysql.connector.connect(
                                            host='localhost',
                                            user='root',
                                            passwd=password,
                                            database='evaluations',
                                            )
my_cursor = mydb.cursor()


# SELECT: formatting result

my_cursor.execute('SELECT * FROM movies_evaluations')
result = my_cursor.fetchall()
print('ID', '\t{:35}'.format('TITLE'), '\tSCORE')
print('--', '\t{:35}'.format('-----'), '\t-----')
for row in result:
    print(row[0], "\t{:35}".format(row[1]), "\t{}".format(row[2]))      # reserving space for element


