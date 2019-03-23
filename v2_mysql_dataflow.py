import os.path                          # todo delete when no more need
from collections import Counter         # todo delete when no more need
import mysql.connector


class Title:
    def __init__(self, name):
        self.name = name


class Database:
    def __init__(self, sourcefile):
        self.sourcefile = sourcefile
        assert os.path.isfile(sourcefile), "No source file or invalid sourcefile for database provided!"
        self.openedfile = open(file=sourcefile, mode='r')
        self.db_dict = {}

    def __str__(self):
        """ k.name - k is an instance of 'Title' class, so k.name accesses it's 'name' attr """
        return '\n'.join("{}: {}".format(k.name, v) for (k, v) in self.into_dict().items())

    def into_dict(self):
        """ Transform file into dict with possibly identical titles within unique instances of 'Title' class"""
        for line in self.openedfile:
            k, v = line.strip().split(': ')
            self.db_dict[Title(k.strip('""'))] = int(v.strip())
        return self.db_dict

    def insert_eval(self, title, evaluation):
        """Reopen file in append mode to move cursor to end of file, reopen in read mode to move cursor to beginning"""
        self.openedfile = open(file=self.sourcefile, mode='a')
        self.openedfile.write("\n\"{}\": {}".format(title, evaluation))
        self.openedfile = open(file=self.sourcefile, mode='r')

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


# c = Database()
# # c.insert_eval("The sth", 5)
# print(c)
# print()
# print(c.get_evals('The sth'))
# print(c.cnt_evals("The sth"))
# print(c.avg_evals('The Wire'))
