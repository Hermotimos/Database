import mysql.connector


class Database:
    def __init__(self, source_db):
        self.source_db = source_db
        self.eval_db = mysql.connector.connect(
                                                host='localhost',
                                                user='root',
                                                passwd='forPythonuse//',
                                                database=source_db
                                                )
        self.mycursor = self.eval_db.cursor()

    def __str__(self):
        def get_tables(db_cursor):
            db_cursor.execute("SHOW TABLES")
            tables = set(t[0] for t in db_cursor)
            return tables

        def get_rows(db_cursor, table):
            db_cursor.execute("SELECT * FROM {}".format(table))
            return [row for row in db_cursor]

        def db_tables_union(db_cursor):
            tables = get_tables(db_cursor)
            for table in tables:
                print('-' * 66, '\n', '#' * 22, table, '#' * 22, '\n', '-' * 66)
                print("| {:4} | {:50} |{:2}|".format('id', 'title', 'score'), '\n', '-' * 66)
                rows = get_rows(db_cursor, table)
                for row in rows:
                    row = ''.join("| {:4} | {:50} | {:2} |".format(str(row[0]), row[1], str(row[2])))
                    print(row)

        str(db_tables_union(self.mycursor))


    def get_evals_for_title(self, title):
        evals_for_title = self.mycursor.execute("SELECT title, score FROM ")


        return evals_for_title

    def avg_evals_for_title(self, title):
        cnt = self.cnt_evals(title)
        s = sum(v for k, v in self.into_dict().items() if k.name == title)
        try:
            return round(s/cnt, 2)
        except ZeroDivisionError:
            return None

    def cnt_evals(self, title):
        n = (k.name for k in self.into_dict().keys() if k.name == title)
        return Counter(n)[title]

    def insert_eval(self, title, evaluation):
        """Reopen file in append mode to move cursor to end of file, reopen in read mode to move cursor to beginning"""
        self.openedfile = open(file=self.source_db, mode='a')
        self.openedfile.write("\n\"{}\": {}".format(title, evaluation))
        self.openedfile = open(file=self.source_db, mode='r')




c = Database('evaluations')

def print_all_tables(database):
    try:
        print(database)
    except TypeError:
        pass

print_all_tables(c)