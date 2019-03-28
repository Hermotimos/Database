import mysql.connector


class MySQLDB:
    def __init__(self, host='', user='', password=input("Enter password for chosen database:\n"), database=''):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __open(self):
        self.cnx = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
        self.cursor = self.cnx.cursor()

    def __close(self):
        self.cursor.close()
        self.cnx.close()

    def __do_sqlstatement(self, statement):
        self.__open()
        self.cursor.execute(statement)
        try:
            result = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError:   # if not select-statement, than .fetchall() throws this error
            result = None
        self.cnx.commit()                               # just does nothing by select-statement
        self.__close()
        return result

    def insert_evaluation(self, insert_into='', values=()):
        # todo needs calling function to provide values as tuple (title, score)
        # todo add if else to handle multiple rows inserts with .executemany()
        statement = 'INSERT INTO {} (title, score) VALUES {}'.format(insert_into, values)
        return self.__do_sqlstatement(statement)

    def select(self, select='*', from_='', where='', order_by=''):
        query = 'SELECT {} FROM {} '.format(select, from_)
        if where:
            query += 'WHERE {} '.format(where)
        if order_by:
            query += 'ORDER BY {} '.format(order_by)
        return self.__construct_result(self.__do_sqlstatement(query))

    def __construct_result(self, query_result):
        query_printout = ''
        for row in query_result:
            query_printout += '\n' + '\t'.join(str(elem) for elem in row)
        return query_printout

    def __repr__(self):
        return "MySQL Database: {}\nhost: {}\nuser: {}\npassword: *******\n" \
               "Tables: {}".format(self.database, self.host, self.user, self.list_tables)

    def __str__(self):
        db_printout = ''
        self.__open()
        self.cursor.execute("SHOW TABLES")
        self.list_tables = [t[0] for t in self.cursor]
        for table in self.list_tables:
            db_printout += self.__construct_whole_table(table)
        self.__close()
        return db_printout

    def __construct_whole_table(self, table):
        table_printout = '\n\n{}\n'.format(table).upper()
        table_printout += '--\t{:40}\t-----'.format('-----')
        table_printout += '\nID\t{:40}\tSCORE\n'.format('TITLE')
        table_printout += '--\t{:40}\t-----'.format('-----')
        whole_table = self.__do_sqlstatement('SELECT * FROM {}'.format(table))
        for row in whole_table:
            table_printout += '\n{}\t{:40}\t{}'.format(row[0], row[1], row[2])
        return table_printout



db = MySQLDB(host='localhost', user='root', database='evaluations')

""" TEST __str__ and within it also .construct_whole_table()"""
# print(db)

""" TEST .do_sqlquery() """
# print(db._MySQLDB__do_sqlstatement('SELECT * FROM boardgames_evaluations WHERE score > 8'))

""" TEST .select() """
# print(db.select('title, score', 'tvseries_evaluations', 'score >+ 6', 'score DESC'))
# print(db.select('AVG(score)', 'boardgames_evaluations'))
# print(db.select('AVG(score)', 'boardgames_evaluations', 'score >= 8'))

""" TEST .insert_evaluation() """
db.insert_evaluation('boardgames_evaluations', ('Eurobusiness', 3))
print(db.select(from_='boardgames_evaluations', where='score > 2'))

""" TEST cartesian JOIN """
# print(db.select(from_='movies_evaluations, tvseries_evaluations'))