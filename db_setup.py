"""
    Create 'evaluations' database with random evaluations for predefined titles.

    Steps:
        1. Creates database (drops one if exists).
        2. Creates tables (movies_evaluations, tvseries_evaluations, pcgames_evaluations, boardgames_evaluations).
        3. Populates tables with random number of random-score evaluations for given lists of titles.

    TODO:
        - implement XML and JSON data types
        - implement XPath and JsonPath queries within SQL
"""
import mysql.connector
from random import random


# CONNECT TO MySQL AND CREATE DATABASE

password = input('Enter password to connect to database:\n')
mydb = mysql.connector.connect(host='localhost', user='root', passwd=password)
mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS evaluations")
mycursor.execute("CREATE DATABASE evaluations")
mycursor.execute("SHOW DATABASES")
for db in mycursor:
    print('database: ', db[0])

mydb = mysql.connector.connect(host='localhost', user='root', passwd=password, database='evaluations')
mycursor = mydb.cursor()


# CREATE TABLES

tables_to_create = ['movies_evaluations', 'tvseries_evaluations', 'pcgames_evaluations', 'boardgames_evaluations']

for table in tables_to_create:
    mycursor.execute("DROP TABLE IF EXISTS {}".format(table))

for table in tables_to_create:
    mycursor.execute("CREATE TABLE {} "
                     "("
                     "evaluation_id INT AUTO_INCREMENT PRIMARY KEY,"
                     "title VARCHAR(200) NOT NULL,"
                     "score TINYINT(2) NOT NULL,"
                     "creation_time DATETIME DEFAULT CURRENT_TIMESTAMP"
                     ")".format(table))

mycursor.execute("SHOW TABLES")
for table in mycursor:
    print('table: ', table[0])


# POPULATE TABLES WITH RANDOM NUMBER OF EVALUATIONS HAVING RANDOM EVALUATION SCORE

def generate_evaluations(titles):
    """
    Returns list of erandom evaluations for titles provided as arg.

    Parameters
    ----------
        titles (any iterable type): Iterable with titles.

    Returns
    -------
        list: Returns list of 2-element tuples [(str, int), (str, int), ...] where int is a random number 1-10.
    """
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


insert_into_movies_evaluations = "INSERT INTO movies_evaluations (title, score) VALUES (%s, %s)"
insert_into_tvseries_evaluations = "INSERT INTO tvseries_evaluations (title, score) VALUES (%s, %s)"
insert_into_pcgames_evaluations = "INSERT INTO pcgames_evaluations (title, score) VALUES (%s, %s)"
insert_into_boardgames_evaluations = "INSERT INTO boardgames_evaluations (title, score) VALUES (%s, %s)"

all_evals = [
            random_evals_movies,
            random_evals_tvseries,
            random_evals_pcgames,
            random_evals_boardgames
            ]
all_insert_statements = [
                        insert_into_movies_evaluations,
                        insert_into_tvseries_evaluations,
                        insert_into_pcgames_evaluations,
                        insert_into_boardgames_evaluations
                        ]
for elem in range(4):
    mycursor.executemany(all_insert_statements[elem], all_evals[elem])


mydb.commit()
