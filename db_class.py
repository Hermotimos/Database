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
            db_printout += self.construct_table(table)
        return db_printout

    def construct_table(self, table):
        table_printout = '\n\n{}\n'.format(table).upper()
        table_printout += '--\t{:40}\t-----'.format('-----')
        table_printout += '\nID\t{:40}\tSCORE\n'.format('TITLE')
        table_printout += '--\t{:40}\t-----'.format('-----')
        rows = self.sqlquery(table=table)
        for row in rows:
            table_printout += '\n{:}\t{:40}\t{}'.format(row[0], row[1], row[2])
        return table_printout

    def sqlquery(self, columns='*', table='', where='', order_by=''):
        query = 'SELECT {} FROM {} '.format(columns, table)
        if where != '':
            query += 'WHERE {} '.format(where)
        if order_by != '':
            query += 'ORDER BY {} '.format(order_by)
        return self.do_sqlquery(query)

    def do_sqlquery(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()



d = MySQLDB(host='localhost', user='root', database='evaluations')
# print('\nTest .sqlquery()', d.sqlquery('evaluation_id', 'movies_evaluations'))            # todo NOT YET DONE
# print('\nTest .construct_table()', d.construct_table('tvseries_evaluations'))
# print('\nTest __str__', d)

print(d.do_sqlquery('SELECT * FROM boardgames_evaluations WHERE score > 8'))
print('\nTest .sqlquery()', d.sqlquery('title, score', 'tvseries_evaluations', 'score >+ 6', 'score DESC'))