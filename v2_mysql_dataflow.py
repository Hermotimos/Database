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
        self.mycursor.execute("SELECT * FROM movies_evaluations")
        return '\n'.join("{} | {} | {}".format(eval_id, title, score) for eval_id, title, score in self.mycursor)




    def get_evals(self, title):
        evals = ''
        for k, v in self.into_dict().items():
            if k.name == title:
                evals += "{}: {}{}".format(k.name, v, '\n')
        return evals

    def avg_evals(self, title):
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
print(c)