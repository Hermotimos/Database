import mysql.connector


class MySQLDB:
    def __init__(self, host='', user='', password=input("Enter password for chosen database:\n"), database=''):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.connection = mysql.connector.connect(
                                                    host=host,
                                                    user=user,
                                                    passwd=password,
                                                    database=database,
                                                    )
        self.cursor = self.connection.cursor()

    def __repr__(self):
        self.cursor.execute("SHOW TABLES")
        return "MySQL Database: {}\n" \
               "host: {}\n" \
               "user: {}\n" \
               "password: *******\n" \
               "Tables: {}".format(self.database, self.host, self.user, [t[0] for t in self.cursor])


d = MySQLDB(host='localhost', user='root', database='evaluations')

# d.cursor.execute('SHOW DATABASES')
print(d)
# for table in d:
#     print(table)
# print(repr(d))