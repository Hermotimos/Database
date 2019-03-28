from db_class import MySQLDB


def choose_table():
    """returns str with table name or 'ALL' for printout of whole db"""

    try:
        data = int(input("Which evaluations would you like to browse?\n"
                         "1 - TV series\n"
                         "2 - movies\n"
                         "3 - PC games\n"
                         "4 - boardgames\n"
                         "5 - all of the above\n"))
        if data == 1:
            table = 'movies_evaluations'
        elif data == 2:
            table = 'tvseries_evaluations'
        elif data == 3:
            table = 'pcgames_evaluations'
        elif data == 4:
            table = 'boardgames_evaluations'
        elif data == 5:
            table = 'ALL'                              # todo watch out: how to handle this later...?
        else:
            raise Exception
        return table
    except Exception:
        print("Wrong value entered. Please choose again.\n")
        return choose_table()


def choose_action():
    """ Returns int 1-8 """
    try:
        chosen_action = int(input("What would you like to do?\n"
                                  "1 - show all evaluations\n"
                                  "2 - show titles with best average evaluation scores\n"
                                  "3 - show all titles with their average evaluation score\n"      # further options
                                  "4 - show all evaluations for a title\n"
                                  "5 - show number of evaluations for a title\n"
                                  "6 - show average evaluation score for a title\n"
                                  "7 - show highest average evaluation score for a title\n"
                                  "8 - show lowest average evaluation score for a title"
                                  "9 - add new evaluation\n"))
        options = [1, 2, 3, 4, 5, 6, 7, 8]
        assert 0 < chosen_action < options[-1] + 1
        return chosen_action
    except Exception:
        print("Wrong value entered. Please choose again.\n")
        return choose_action()


def do_action():
    db = MySQLDB(host='localhost', user='root', database='evaluations')

    chosen_table = choose_table()
    if chosen_table == 'ALL':
        print(db)
    else:
        chosen_action = choose_action()
        if chosen_action == 1:                          # if or elif ??
            db.select(from_=chosen_table)
        elif chosen_action == 2:
            pass                    # todo further options (eval over n; titles with top n avg-evals etc)
        elif chosen_action == 3:
            db.select(select='title, AVG(score)', from_=chosen_table, group_by='title')
        elif chosen_action == 4:
            title = ask_for_title()
            db.select(select='title, score', from_=chosen_table, where='title = {}'.format(title))
        elif chosen_action == 5:
            title = ask_for_title()
            db.select(select='COUNT(title)', from_=chosen_table, where='title = {}'.format(title))
        elif chosen_action == 6:
            title = ask_for_title()
            db.select(select='AVG(title)', from_=chosen_table, where='title = {}'.format(title))
        elif chosen_action == 7:
            db.select(select='title, MAX(score)', from_=chosen_table, where='score = MAX(score)')
        elif chosen_action == 8:
            db.select(select='title, MIN(score)', from_=chosen_table, where='score = MAX(score)')
        elif chosen_action == 9:
            evaluate(db, chosen_table)                                                                          # todo


def evaluate(database, table):
    new_tit = ask_for_title()
    new_eval = ask_for_evaluation()
    values = (new_tit, new_eval)
    database.insert_evaluation(insert_into=''.format(table), values=values)
    print("Your evaluation: '{}': {} \nYour evaluation is much appreciated.".format(new_tit, new_eval))


def ask_for_title():
    title = input("Enter title: ")
    try:
        assert len(title) > 0
        return title
    except AssertionError:
        print("You have not given any title. Try again :)\n")
        return ask_for_title()


def ask_for_evaluation():
    new_evaluation = input("Enter evaluation 1-10: ")
    try:
        assert 0 < int(new_evaluation) < 11
        return new_evaluation
    except Exception:
        print("Your note ({}) outside the scope of possible evaluations (1-10).\nTry again :)\n".format(new_evaluation))
        return ask_for_evaluation()
