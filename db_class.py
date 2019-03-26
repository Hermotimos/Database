import mysql.connector


class MySQLDB:
    def __init__(self, host='', user='', password=input("Enter password for chosen database:\n"), database=''):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.connection = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
        self.cursor = self.connection.cursor()

        self.cursor.execute("SHOW TABLES")
        self.list_tables = [t[0] for t in self.cursor]

    def __repr__(self):
        return "MySQL Database: {}\n" \
               "host: {}\n" \
               "user: {}\n" \
               "password: *******\n" \
               "Tables: {}".format(self.database, self.host, self.user, self.list_tables)

    def __str__(self):
        def get_rows(cursor, table):
            cursor.execute("SELECT * FROM {}".format(table))
            return [row for row in cursor]

        def db_tables_union(cursor):
            printout =
            for table in self.list_tables:
                printout.append(table)
                rows = get_rows(cursor, table)
                for row in rows:
                    printout.append(row)
            return printout

        lst = db_tables_union(self.cursor)

        return str([row for row in lst])


d = MySQLDB(host='localhost', user='root', database='evaluations')

# d.cursor.execute('SHOW DATABASES')
print(d)
# for table in d:
#     print(table)
# print(repr(d))