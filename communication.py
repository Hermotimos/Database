from db_class import MySQLDB


def choose_table():
    try:
        data = int(input("Which evaluations would you like to browse?\n"
                         "1 - TV series\n"
                         "2 - movies\n"
                         "3 - PC games\n"
                         "4 - boardgames\n"
                         "5 - all of the above\n"))
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
            raise Exception
        return table
    except Exception:
        print("Wrong value entered. Please choose again.\n")
        return choose_table()


def choose_action():
    try:
        chosen_action = int(input("What would you like to do?\n"
                                  "1 - show all evaluations\n"
                                  "2 - show titles with best average evaluation scores\n"
                                  "3 - show all titles with their average evaluation score\n"     
                                  "4 - show all evaluations for a title\n"
                                  "5 - show number of evaluations for a title\n"
                                  "6 - show average evaluation score for a title\n"
                                  "7 - show highest evaluation score for a title\n"
                                  "8 - show lowest evaluation score for a title\n"
                                  "9 - add new evaluation\n"))
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
        if chosen_action == 1:
            print(db.select(from_=chosen_table))
        elif chosen_action == 2:
            pass                    # todo further options (eval over n; titles with top n avg-evals etc)
        elif chosen_action == 3:
            print(db.select(select='title, ROUND(AVG(score), 1)', from_=chosen_table, group_by='title'))
        elif chosen_action == 4:
            res = db.select(select='title, score', from_=chosen_table, where='title = \'{}\''.format(ask_title()))
            ispresent(res)
        elif chosen_action == 5:
            res = db.select(select='COUNT(title)', from_=chosen_table, where='title = \'{}\''.format(ask_title()))
            ispresent(res)
        elif chosen_action == 6:
            res = db.select(select='title, AVG(score)', from_=chosen_table, where='title = \'{}\''.format(ask_title()))
            ispresent(res)
        elif chosen_action == 7:
            res = db.select(select='title, MAX(score)', from_=chosen_table, where='title = \'{}\''.format(ask_title()))
            ispresent(res)
        elif chosen_action == 8:
            res = db.select(select='title, MIN(score)', from_=chosen_table, where='title = \'{}\''.format(ask_title()))
            ispresent(res)
        elif chosen_action == 9:
            evaluate(db, chosen_table)


def ispresent(sql_result):
    if len(sql_result) > 0:
        print(sql_result)
    else:
        print("There aren't any evaluations for given title in the database.")


def evaluate(database, table):
    new_tit = str(ask_title())
    new_eval = int(ask_evaluation())
    values = (new_tit, new_eval)
    database.insert_evaluation(insert_into='{}'.format(table), values=values)
    print("Evaluation: ['{}': {}] has been added.\nYour evaluation is much appreciated.".format(new_tit, new_eval))


def ask_title():
    title = input("Enter title: ")
    try:
        assert len(title) > 0
        return title
    except AssertionError:
        print("You have not given any title. Try again :)\n")
        return ask_title()


def ask_evaluation():
    new_evaluation = input("Enter evaluation 1-10: ")
    try:
        assert 0 < int(new_evaluation) < 11
        return new_evaluation
    except Exception:
        print("Your note ({}) outside the scope of possible evaluations (1-10).\nTry again :)\n".format(new_evaluation))
        return ask_evaluation()
