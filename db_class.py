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
        db_printout = ''
        for table in self.list_tables:
            db_printout += self.get_table(table)
        return db_printout

    def get_table(self, table):
        table_printout = '\n\n{}\n'.format(table).upper()
        table_printout += '--\t{:40}\t-----'.format('-----')
        table_printout += '\nID\t{:40}\tSCORE\n'.format('TITLE')
        table_printout += '--\t{:40}\t-----'.format('-----')
        self.cursor.execute("SELECT * FROM {}".format(table))
        table_printout += self.get_rows(self.cursor)
        return table_printout

    def get_rows(self, query_result):
        rows_printout = ''
        for row in query_result:
            rows_printout += '\n{:}\t{:40}\t{}'.format(row[0], row[1], row[2])
        return rows_printout


    def query(self, columns='*', table='', where=''):
        query = 'SELECT {} FROM {} '.format(columns, table)
        if where != '':
            query += 'WHERE {} '.format(where)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


d = MySQLDB(host='localhost', user='root', database='evaluations')
# print('\nTest .query()', d.query('evaluation_id', 'movies_evaluations'))            # todo NOT YET DONE
# print('\nTest .get_table()', d.get_table('tvseries_evaluations'))
print('\nTest __str__', d)
