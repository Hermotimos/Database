# EvaluationsDB

## Table of contents
* [General info](#general-info)  
* [Technologies](#technologies)  
* [Setup](#setup)  
* [Status](#status)  
* [Features](#features)
* [Content](#content)  
* [Sources and inspirations](#sources-and-inspirations)


## General info
This project was created for learning and exercise purposes.  
This program enables user to connect to 'evaluations' database in order to browse the database and insert new evaluations.

## Technologies
Python 3.7  
SQL

## Setup
Program created and run in IDE (PyCharm 2019.1.1 Community Edition) under Windows 7.

## Features
* show whole database  
* show TOP 5 titles with best average evaluation scores  
* show all titles with their average evaluation score  
* show all evaluations for a title  
* show number of evaluations for a title  
* show average evaluation score for a title  
* show highest/lowest evaluation score for a title  
* add new evaluation

## Content

### create_database.py
Standalone program for creating database, tables and populating tables with random evaluations for a bunch of titles.
### db_class.py
Defines connection to MySQL database as class. Creates methods to query MySQL database.
### communications.py
Functions using methods of MySQL database class to query it and insert new evaluations according to user's input.
### start.py
Main module. 

## Status
TODO: add option to query (not only print) all tables of the database together (JOIN).  
TODO: include XML and JSON data types in SQL schema.  
TODO: implement XPath and JSONPath expressions in SQL queries and inserts.  
TODO: develop reusable MySQLDatabase class.  

## Sources and inspirations
* https://www.flynerd.pl/2017/05/python-4-typy-i-zmienne.html  
* https://github.com/nestordeharo/mysql-python-class/blob/master/mysql_python.py#L2  
* https://www.w3schools.com/python/python_mysql_getstarted.asp  
