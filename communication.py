"""
    This module serves interaction between user and database.

    SECTION I: action-functions
    ------------------------
    Defines functions that present user with action options and perform chosen actions on database.
    Eables user to choose between databases for TV series, movies, PC games and boardgames, as well as
    what action to perform (ex. show data bout specific title, show TOP 5, leave new evaluation).

    do_action(): Main function is this section, exported to start.py.
               Uses MySQLDB class methods to query and update database.


    SECTION II: input-functions
    ------------------------
    Defines input functions for interaction with user.
    All functions in this section call themselves recursively in case user enters value from outside choice options.

    ask_continue(): Exported to start.py. Enables user to continue current session ad infinitum.
"""

import time
from db_class import MySQLDB


# >>>>>>>>>>>>>>>>>>>>>>>>> SECTION I: action-functions <<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def choose_table():
    try:
        data = int(input("Which evaluations would you like to browse?\n"
                         "1 - TV series\n"
                         "2 - movies\n"
                         "3 - PC games\n"
                         "4 - boardgames\n"
                         "5 - print whole database\n"))
        if   data == 1: table = 'tvseries_evaluations'
        elif data == 2: table = 'movies_evaluations'
        elif data == 3: table = 'pcgames_evaluations'
        elif data == 4: table = 'boardgames_evaluations'
        elif data == 5: table = 'ALL'
        else:
            raise ValueError
        return table
    except ValueError:
        print("Wrong value entered. Please choose again.\n")
        return choose_table()


def choose_action():
    try:
        options = range(1, 10)
        chosen_action = input("What would you like to do?\n"
                              "{} - show all evaluations\n"
                              "{} - show TOP 5 titles with best average evaluation scores\n"
                              "{} - show all titles with their average evaluation score\n"     
                              "{} - show all evaluations for a title\n"
                              "{} - show number of evaluations for a title\n"
                              "{} - show average evaluation score for a title\n"
                              "{} - show highest evaluation score for a title\n"
                              "{} - show lowest evaluation score for a title\n"
                              "{} - add new evaluation\n".format(*options))
        assert 0 < int(chosen_action) < options[-1] + 1
        return int(chosen_action)
    except (AssertionError, ValueError):
        print("Wrong value entered. Please choose again.\n")
        return choose_action()


def do_action():
    # todo: awful function but how should it be changed? (for future development)
    db = MySQLDB(host='localhost', user='root', database='evaluations')
    chosen_table = choose_table()

    if chosen_table == 'ALL':
        print(db)
    else:
        chosen_action = choose_action()
        timelimit = ''
        if chosen_action != 9:
            timelimit = ask_timelimit()

        if chosen_action == 1:
            result = db.select(from_=chosen_table, where=timelimit)
            is_not_empty(result)

        elif chosen_action == 2:
            result = db.select(select='title, ROUND(AVG(score), 1)',
                               from_=chosen_table,
                               where=timelimit,
                               order_by='AVG(score) DESC',
                               group_by='title',
                               limit=5)
            is_not_empty(result)

        elif chosen_action == 3:
            result = db.select(select='title, ROUND(AVG(score), 1)',
                               from_=chosen_table,
                               where=timelimit,
                               group_by='title')
            is_not_empty(result)

        elif chosen_action == 4:
            result = db.select(select='title, score',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title("Enter title: "), timelimit))
            is_not_empty(result)

        elif chosen_action == 5:
            result = db.select(select='COUNT(title)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title("Enter title: "), timelimit))
            is_not_empty(result)

        elif chosen_action == 6:
            result = db.select(select='title, AVG(score)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title("Enter title: "), timelimit))
            is_not_empty(result)

        elif chosen_action == 7:
            result = db.select(select='title, MAX(score)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title("Enter title: "), timelimit))
            is_not_empty(result)

        elif chosen_action == 8:
            result = db.select(select='title, MIN(score)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title("Enter title: "), timelimit))
            is_not_empty(result)

        elif chosen_action == 9:
            evaluate(db, chosen_table)


def is_not_empty(sql_result):
    if len(sql_result) > 0:
        print(sql_result)
    else:
        print("There aren't any evaluations in the database that satisfy given conditions.")


def evaluate(database, table):
    new_tit = ask_title("Enter title: ")
    new_eval = ask_evaluation("Enter evaluation from 1 to 10: ")
    values = (new_tit, new_eval)
    database.insert_evaluation(insert_into='{}'.format(table), values=values)
    print("Evaluation: ['{}': {}] has been added.\nYour evaluation is much appreciated.".format(new_tit, new_eval))


# >>>>>>>>>>>>>>>>>>>>>>>>> SECTION II: question-functions <<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def ask_yes_or_no(prompt):
    """Ask user question in 'prompt' and return True or False depending on answer.

    Question will be asked recursively until user's input is 'y' or 'n'.

    Parameters
    ----------
        prompt (str): Text of question printed to the user.

    Returns
    -------
        bool: True or False depending on user answer ('y' or 'n').
    """
    answer = input(prompt)
    try:
        assert answer in ('y', 'n')
        return True if answer == 'y' else False
    except AssertionError:
        print("Wrong value entered. Please choose again.\n")
        return ask_yes_or_no(prompt)


def ask_title(prompt):
    """Ask user to enter title.

    Question will be asked recursively until user's input is at least one digit long.

    Parameters
    ----------
        prompt (str): Text of question printed to the user.

    Returns
    -------
        str: Title entered by user.
    """
    title = input(prompt)
    try:
        assert len(title) > 0
        return title
    except AssertionError:
        print("You have not given any title. Try again :)\n")
        return ask_title(prompt)


def ask_evaluation(prompt):
    """Ask user to enter evaluation 1-10.

    Question will be asked recursively until user's input is a number from 1 to 10.

    Parameters
    ----------
        prompt (str): Text of question printed to the user.

    Returns
    -------
        int: User's evaluation, number from 1 to 10.
    """
    new_evaluation = input(prompt)
    try:
        assert 0 < int(new_evaluation) < 11
        return int(new_evaluation)
    except (AssertionError, ValueError):
        print("Your note ({}) outside the scope of possible evaluations (1-10).\nTry again :)\n".format(
            new_evaluation))
        return ask_evaluation(prompt)


def ask_timelimit():

    def ask_date(prompt):
        """Ask user to enter date in format yyyy-mm-dd.

        Question will be asked recursively until user enters date in format yyyy-mm-dd.

        Parameters
        ----------
            prompt (str): The exact question about date asked to user.

        Returns
        -------
            str: Date in yyyy-mm-dd format.

        """
        date = input("{}\n".format(prompt))
        if not date:
            return ''
        else:
            try:
                time.strptime(date, '%Y-%m-%d')
                return date
            except ValueError:
                print("Wrong value entered. Please choose again.\n")
                return ask_date(prompt)

    limit = ask_yes_or_no("Would you like to limit results to specific time period (y or n) ?\n")
    if limit:
        low = ask_date("Specify lower boundary of time period (format: yyyy-mm-dd) or press ENTER for none.\n")
        upp = ask_date("Specify upper boundary of time period (format: yyyy-mm-dd) or press ENTER for none.\n")
        if not low:
            low = '1900-01-01'
        if not upp:
            upp = 'NOW()'
        return "creation_time BETWEEN '{}' AND '{}' ".format(low, upp)
    else:
        return "creation_time BETWEEN '1900-01-01' AND NOW() "


def ask_continue():
    answ = ask_yes_or_no("\nWould you like to continue (y/n) ?\n")
    return True if answ else False
