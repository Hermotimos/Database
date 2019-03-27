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
        return "MySQL Database: {}\nhost: {}\nuser: {}\npassword: *******\n" \
               "Tables: {}".format(self.database, self.host, self.user, self.list_tables)

    def __str__(self):
        db_printout = ''
        for table in self.list_tables:
            db_printout += self.__construct_whole_table(table)
        return db_printout

    def __construct_whole_table(self, table):
        table_printout = '\n\n{}\n'.format(table).upper()
        table_printout += '--\t{:40}\t-----'.format('-----')
        table_printout += '\nID\t{:40}\tSCORE\n'.format('TITLE')
        table_printout += '--\t{:40}\t-----'.format('-----')
        whole_table = self.__do_query('SELECT * FROM {}'.format(table))
        for row in whole_table:
            table_printout += '\n{}\t{:40}\t{}'.format(row[0], row[1], row[2])
        return table_printout

    def sqlquery(self, select='*', from_='', where='', order_by=''):
        query = 'SELECT {} FROM {} '.format(select, from_)
        if where != '':
            query += 'WHERE {} '.format(where)
        if order_by != '':
            query += 'ORDER BY {} '.format(order_by)
        return self.__construct_result(self.__do_query(query))

    def __do_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __construct_result(self, query_result):
        query_printout = ''
        for row in query_result:
            query_printout += '\n' + '\t'.join(str(elem) for elem in row)
        return query_printout

    def insert_evaluation(self, insert_into='', values=()):
        # todo needs calling function to provide values as tuple (title, score)
        statement = 'INSERT INTO {} (title, score) VALUES {}'.format(insert_into, values)
        self.cursor.execute(statement)
        self.connection.commit()
        return None



db = MySQLDB(host='localhost', user='root', database='evaluations')

""" TEST .construct_whole_table() and __str__ """
# print('\nTest .__construct_whole_table()', db.__construct_whole_table('tvseries_evaluations'))
# print('\nTest __str__', db)

""" TEST .do_sqlquery() """
# print(db.__do_query('SELECT * FROM boardgames_evaluations WHERE score > 8'))

""" TEST .sqlquery() """
# print('\nTest .sqlquery()', db.sqlquery('title, score', 'tvseries_evaluations', 'score >+ 6', 'score DESC'))
# print(db.sqlquery('AVG(score)', 'boardgames_evaluations'))
# print(db.sqlquery('AVG(score)', 'boardgames_evaluations', 'score >= 8'))

""" TEST .insert_evaluation() """
# db.insert_evaluation('boardgames_evaluations', ('Eurobusiness', 2))
# print(db.sqlquery(from_='boardgames_evaluations'))

""" TEST cartesian JOIN """
print(db.sqlquery(from_='movies_evaluations, tvseries_evaluations'))