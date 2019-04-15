"""
    This module defines MySQLDB class, which connect user to MySQL database created in db_setup.py.

    MySQLDB class enables basic SELECT... FROM... and INSERT INTO... VALUES... statements
    Following SQL clauses are supported in SELECT...FROM... statements:
        - WHERE
        - GROUP BY
        - ORDER BY
        - LIMIT

    TODO:
        - implement paging with LIMIT and OFFSET
        - implement JOIN-s for querying all tables (requires new option in communication.py)
"""


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
        statement = 'INSERT INTO {} (title, score) VALUES {}'.format(insert_into, values)
        return self.__do_sqlstatement(statement)

    def select(self, select='*', from_='', where='', order_by='', group_by='', limit=0):

        def construct_result(query_result):
            query_printout = ''
            for row in query_result:
                query_printout += '\n' + '\t'.join(str(elem) for elem in row)
            return query_printout

        query = 'SELECT {} FROM {} '.format(select, from_)
        if where:
            query += 'WHERE {} '.format(where)
        if group_by:
            query += 'GROUP BY {} '.format(group_by)
        if order_by:
            query += 'ORDER BY {} '.format(order_by)
        if limit:
            query += 'LIMIT {} '.format(limit)
        return construct_result(self.__do_sqlstatement(query))

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
        table_printout += '----\t{:40}\t-----'.format('-----')
        table_printout += '\n ID \t{:40}\tSCORE\n'.format('TITLE')
        table_printout += '----\t{:40}\t-----'.format('-----')
        whole_table = self.__do_sqlstatement('SELECT * FROM {}'.format(table))
        for row in whole_table:
            table_printout += '\n{:4}\t{:40}\t{:-2}'.format(row[0], row[1], row[2])
        return table_printout
