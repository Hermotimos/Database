import mysql.connector
from random import random

password = input('Enter password to connect to database:\n')
mydb = mysql.connector.connect(host='localhost', user='root', passwd=password)
mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS evaluations")
mycursor.execute("CREATE DATABASE evaluations")
mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db[0])

mydb = mysql.connector.connect(host='localhost', user='root', passwd=password, database='evaluations')
mycursor = mydb.cursor()


"""CREATE TABLES"""

mycursor.execute("DROP TABLE IF EXISTS movies_evaluations")
mycursor.execute("DROP TABLE IF EXISTS tvseries_evaluations")
mycursor.execute("DROP TABLE IF EXISTS pcgames_evaluations")
mycursor.execute("DROP TABLE IF EXISTS boardgames_evaluations")

mycursor.execute("CREATE TABLE movies_evaluations "
                 "("
                 "evaluation_id INT AUTO_INCREMENT PRIMARY KEY,"
                 "title VARCHAR(200) NOT NULL,"
                 "score TINYINT(2) NOT NULL"
                 ")")
mycursor.execute("CREATE TABLE tvseries_evaluations "
                 "("
                 "evaluation_id INT AUTO_INCREMENT PRIMARY KEY,"
                 "title VARCHAR(200) NOT NULL,"
                 "score TINYINT(2) NOT NULL"
                 ")")
mycursor.execute("CREATE TABLE pcgames_evaluations "
                 "("
                 "evaluation_id INT AUTO_INCREMENT PRIMARY KEY,"
                 "title VARCHAR(200) NOT NULL,"
                 "score TINYINT(2) NOT NULL"
                 ")")
mycursor.execute("CREATE TABLE boardgames_evaluations "
                 "("
                 "evaluation_id INT AUTO_INCREMENT PRIMARY KEY,"
                 "title VARCHAR(200) NOT NULL,"
                 "score TINYINT(2) NOT NULL"
                 ")")
mycursor.execute("SHOW TABLES")
for table in mycursor:
    print(table[0])


""" POPULATE TABLES WITH RANDOM NUMBER OF EVALUATIONS HAVING RANDOM EVALUATION SCORE"""


def generate_evaluations(titles):
    """ Returns list of 2-element tuples (title, evaluation) """
    random_evaluations = []
    for title in titles:
        n = 0
        while n <= round(random()*(10-1)+1, 0):
            random_evaluations.append((title, round(random()*(10-1)+1, 0)))
            n += 1
    return random_evaluations


movies_titles = [
                  'Blade Runner',
                  'Contact',
                  'Interstellar',
                  'Truman Show',
                  'Arrival',
                  'Solaris',
                  'Ex Machina',
                  'Eternal Sunshine of The Spotless Mind',
                  'Her',
                  'Moon',
                  'Dune'
                ]
tvseries_titles = [
                    'The Wire',
                    'The Shield',
                    'Battlestar Galactica',
                    'Twin Peaks',
                    'True Detective',
                    'Game of Thrones',
                    'The Expanse',
                    'Altered Carbon',
                    'Deadwood',
                    'Sons of Anarchy',
                    'Taboo'
                    ]
pcgames_titles = [
                  'Medieval Total War',
                  'Shogun Total War',
                  'Shogun 2 Total War',
                  'Medieval 2 Total War',
                  'Rome Total War',
                  'Diablo',
                  'Diablo 2',
                  'Icewind Dale 2',
                  'Fallout',
                  'Heroes of Might And Magic III',
                  'Quake III: Arena',
                ]
boardgames_titles = [
                        'Battlestar Galactica',
                        'Game of Thrones',
                        'Carcassonne',
                        'Dixit',
                        'Magiczny Miecz',
                        'The Settlers of Catan'
                    ]

random_evals_movies = generate_evaluations(movies_titles)
random_evals_tvseries = generate_evaluations(tvseries_titles)
random_evals_pcgames = generate_evaluations(pcgames_titles)
random_evals_boardgames = generate_evaluations(boardgames_titles)

insert_into_movies_evaluations = "INSERT INTO movies_evaluations (title, score)" \
                   "VALUES (%s, %s)"
insert_into_tvseries_evaluations = "INSERT INTO tvseries_evaluations (title, score)" \
                   "VALUES (%s, %s)"
insert_into_pcgames_evaluations = "INSERT INTO pcgames_evaluations (title, score)" \
                   "VALUES (%s, %s)"
insert_into_boardgames_evaluations = "INSERT INTO boardgames_evaluations (title, score)" \
                   "VALUES (%s, %s)"

mycursor.executemany(insert_into_movies_evaluations, random_evals_movies)
mycursor.executemany(insert_into_tvseries_evaluations, random_evals_tvseries)
mycursor.executemany(insert_into_pcgames_evaluations, random_evals_pcgames)
mycursor.executemany(insert_into_boardgames_evaluations, random_evals_boardgames)
mydb.commit()
