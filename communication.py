from db_class import MySQLDB
from questions import ask_date, ask_evaluation, ask_title, ask_yes_or_no


def choose_table():
    try:
        data = int(input("Which evaluations would you like to browse?\n"
                         "1 - TV series\n"
                         "2 - movies\n"
                         "3 - PC games\n"
                         "4 - boardgames\n"
                         "5 - print whole database\n"))
        if data == 1:
            table = 'tvseries_evaluations'
        elif data == 2:
            table = 'movies_evaluations'
        elif data == 3:
            table = 'pcgames_evaluations'
        elif data == 4:
            table = 'boardgames_evaluations'
        elif data == 5:
            table = 'ALL'
        else:
            raise ValueError
        return table
    except ValueError:
        print("Wrong value entered. Please choose again.\n")
        return choose_table()


def choose_action():
    try:
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
        return chosen_action
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
            print(db.select(select='title, ROUND(AVG(score), 1)',
                            from_=chosen_table,
                            where=timelimit,
                            group_by='title'))

        elif chosen_action == 4:
            result = db.select(select='title, score',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title(), timelimit))
            is_not_empty(result)

        elif chosen_action == 5:
            result = db.select(select='COUNT(title)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title(), timelimit))
            is_not_empty(result)

        elif chosen_action == 6:
            result = db.select(select='title, AVG(score)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title(), timelimit))
            is_not_empty(result)

        elif chosen_action == 7:
            result = db.select(select='title, MAX(score)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title(), timelimit))
            is_not_empty(result)

        elif chosen_action == 8:
            result = db.select(select='title, MIN(score)',
                               from_=chosen_table,
                               where='title = \'{}\' AND {}'.format(ask_title(), timelimit))
            is_not_empty(result)

        elif chosen_action == 9:
            evaluate(db, chosen_table)


def is_not_empty(sql_result):
    if len(sql_result) > 0:
        print(sql_result)
    else:
        print("There aren't any evaluations in the database that satisfy given conditions.")


def evaluate(database, table):
    new_tit = str(ask_title())
    new_eval = int(ask_evaluation())
    values = (new_tit, new_eval)
    database.insert_evaluation(insert_into='{}'.format(table), values=values)
    print("Evaluation: ['{}': {}] has been added.\nYour evaluation is much appreciated.".format(new_tit, new_eval))


def ask_timelimit():
    limit = ask_yes_or_no("Would you like to limit results to specific time period (y or n) ?\n")
    if limit:
        low = ask_date("Specify lower boundary of time period (format: yyyy-mm-dd) or press ENTER for none.\n")
        upp = ask_date("Specify upper boundary of time period (format: yyyy-mm-dd) or press ENTER for none.\n")
        if not low:
            low = '1900-01-01'
        if not upp:
            upp = 'NOW()'
        return "creation_time BETWEEN '{}' AND {} ".format(low, upp)
    else:
        return "creation_time BETWEEN '1900-01-01' AND NOW() "


# todo: similar function with prompt and assertion to check ?
