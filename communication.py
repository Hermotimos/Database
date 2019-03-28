from db_class import MySQLDB


def choose_db():
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
        return choose_db()


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
    chosen_db = choose_db()
    chosen_action = choose_action()
    db = MySQLDB(host='localhost', user='root', database='evaluations')

    if chosen_action == 1:
        print(db)
    elif chosen_action == 2:
        pass                    # todo further options (eval over n; titles with top n avg-evals etc)
    elif chosen_action == 3:
        db.select(select='title, AVG(score)', from_=chosen_db, group_by='title')
    elif chosen_action == 4:
        db.select(select='title, score', from_=chosen_db, where='title = xxxxx')      # todo separate function
    elif chosen_action == 5:
        db.select(select='COUNT(title)', from_=chosen_db, where='title = xxxxx')      # todo separate function
    elif chosen_action == 6:
        db.select(select='AVG(title)', from_=chosen_db, where='title = xxxxx')        # todo separate function
    elif chosen_action == 7:
        db.select(select='title, MAX(score)', from_=chosen_db, where='score = MAX(score)')
    elif chosen_action == 8:
        db.select(select='title, MIN(score)', from_=chosen_db, where='score = MAX(score)')
    elif chosen_action == 9:
        pass                                                                          # todo separate function
