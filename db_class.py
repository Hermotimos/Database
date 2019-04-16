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
    def __init__(self, host, user, database, password=input("Enter password for chosen database:\n")):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __open(self):
        """Create connection to database and create cursor object."""
        self.cnx = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
        self.cursor = self.cnx.cursor()

    def __close(self):
        """Close cursor, then close connection to the database."""
        self.cursor.close()
        self.cnx.close()

    def insert_evaluation(self, insert_into='', values=()):
        """Construct SQL DML statement as str, call __do_sqlstatement() to perform on database, return query result.

        Parameters
        ----------
            insert_into (str): Name of a table in the database.
            values (tuple): The method defines target columns for INSERT statement as (title, score).
                            The number and the order of values has to match target columns' order and number.

        Returns
        -------
            str: Result of __do_sqlstatement(), ex.: 1 row(s) inserted.
        """
        statement = 'INSERT INTO {} (title, score) VALUES {}'.format(insert_into, values)
        return self.__do_sqlstatement(statement)

    def select(self, select='*', from_='', where='', order_by='', group_by='', limit=0):
        """Construct SQL DQL statement as str, perform query on database, return formatted query result.

        Parameters
        ----------
            select: Names of queried columns; default '*' stands for ALL.
            from_: Name of queried table.
            where: Conditions limiting query result.
            order_by: Key for ordering query result.
            group_by: Key for grouping rows ins query result.
            limit: Key for limiting query result to first n rows only; default 0 stands for no limit.

        Returns
        -------
            str: Formatted query result - line per row of query result.
                 Final result is formatted by nested function format_result().
        """

        def format_result(query_result):
            """Unpack list of tuples with SQL query result and format it as multi-line str.

            Unpacks each tuple representing one row of query result and converts its elements to str.
            From each unpacked row/tuple, a new str line is constructed and added to multi-line str to be returned.

            Parameters
            ----------
                query_result (list of tuples): SQL query result.
                                               [(int, str, int, datetime.datetime(int, int, int, int, int, int)), ...]
            Returns
            -------
                str:  One- to n-lines long str.

            Examples
            --------
                [(1, 'Blade Runner', 6, datetime.datetime(2019, 3, 30, 16, 14, 27)),
                (2, 'Blade Runner', 5, datetime.datetime(2019, 3, 30, 16, 14, 27))]
                =>
                '1   Blade Runner                      6 	2019-03-30 16:14:27'
                '2   Blade Runner                      5 	2019-03-30 16:14:27'
            """
            query_printout = ''
            for row in query_result:
                query_printout += '\n' + '\t'.join(str(field) for field in row)
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
        return format_result(self.__do_sqlstatement(query))

    def __do_sqlstatement(self, statement):
        """Perform SQL statement on the database and return result.

        This method serves for SELECT...FROM... and INSERT...INTO... statements.
        If statement is INSERT INTO..., than self.cursor.fetchall() raises 'mysql.connector.errors.InterfaceError',
        therefore try-except block.
        If statement is INSERT INTO..., than self.cnx.commit() has no effect.

        Parameters
        ----------
            statement (str): SQL statement in form of str constructed by insert_evaluation() or select() methods.

        Returns
        -------
            tuple or str:
                For SQL DQL statement (SELECT... FROM...) returns one tuple per row of query result.
                For SQL DML statement (INSERT INTO... VALUES...) returns str with count of rows inserted.

        Examples
        --------
            __do_sqlstatement('SELECT * FROM movies_evaluations LIMIT 3')
            [(1, 'Blade Runner', 6, datetime.datetime(2019, 3, 30, 16, 14, 27)),
            (2, 'Blade Runner', 5, datetime.datetime(2019, 3, 30, 16, 14, 27)),
            (3, 'Blade Runner', 5, datetime.datetime(2019, 3, 30, 16, 14, 27))]

            __do_sqlstatement('INSERT INTO movies_evaluations (title, score) VALUES ('Twin Peaks', 10)')
            1 row(s) inserted.
        """
        self.__open()
        self.cursor.execute(statement)
        try:
            result = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            result = None
            print(f'\n{self.cursor.rowcount} row(s) inserted.')
        self.cnx.commit()
        self.__close()
        return result

    def __repr__(self):
        """Return info about current connection to database and database structure (tables)."""
        return "MySQL Database: {}\nhost: {}\nuser: {}\npassword: *******\n" \
               "Tables: {}".format(self.database, self.host, self.user, self.tables_list)

    def __str__(self):
        """For each table in database format it as str and add to multi-line str for possible printout of __str__.

        Returns
        -------
            str: Multi-line str containing all tables in database

        Examples
        --------
                TVSERIES_EVALUATIONS
                ----	-----                                   	-----
                 ID 	TITLE                                   	SCORE
                ----	-----                                   	-----
                   1	The Wire                                	 9
                   2	The Wire                                	 5
                   ...  ...                                          ...

                BOARDGAMES_EVALUATIONS
                ----	-----                                   	-----
                 ID 	TITLE                                   	SCORE
                ----	-----                                   	-----
                   1	Battlestar Galactica                    	 9
                   2	Battlestar Galactica                    	 4
                   ...  ...                                          ...

        """
        db_printout = ''
        self.__open()
        self.cursor.execute("SHOW TABLES")
        self.tables_list = [t[0] for t in self.cursor]
        for table in self.tables_list:
            db_printout += self.__format_whole_table(table)
        self.__close()
        return db_printout

    def __format_whole_table(self, table_name):
        """Format and return whole SQL table as str for __str__ method.

        Parameters
        ----------
        table_name (str): Name of table in database.

        Returns
        -------
            str: Multi-line str with table header, columns headers and lines representing rows of SQL table.

        Examples
        -------
            __format_whole_table(tvseries_evaluations)

                TVSERIES_EVALUATIONS
                ----	-----                                   	-----
                 ID 	TITLE                                   	SCORE
                ----	-----                                   	-----
                   1	The Wire                                	 9
                   2	The Wire                                	 5
                   ...  ...                                          ...
        """
        table_printout = '\n\n{}\n'.format(table_name).upper()
        table_printout += '----\t{:40}\t-----'.format('-----')
        table_printout += '\n ID \t{:40}\tSCORE\n'.format('TITLE')
        table_printout += '----\t{:40}\t-----'.format('-----')
        whole_table = self.__do_sqlstatement('SELECT * FROM {}'.format(table_name))
        for row in whole_table:
            table_printout += '\n{:4}\t{:40}\t{:-2}'.format(row[0], row[1], row[2])
        return table_printout


# db = MySQLDB(host='localhost', user='root', database='evaluations')
# print(db.do_sqlstatement('SELECT * FROM movies_evaluations'))



result_table = [(1, 'Blade Runner', 6, (2019, 3, 30, 16, 14, 27)),
                (2, 'Blade Rudddddddddnner', 5, (2019, 3, 30, 16, 14, 27)),
                (3, 'Blade Runner', 5, (2019, 3, 30, 16, 14, 27))]

columns_count = len(result_table[0])
columns_widths = {}

for col in range(columns_count):
    columns_widths[col] = max(len(str(row[col])) for row in result_table)
print(columns_widths)

widths_list = [w for w in columns_widths.values()]
print(widths_list)
printout = ''

# for row in result_table:
#     printout += '\n{0:{1}}'.format((field for field in row), (width for width in widths_list))

for row in result_table:
    print(row)
    printout += '\n' + '\t'.join(str(field) for field in row)

print(printout)