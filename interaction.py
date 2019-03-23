from dataflow import Database


def choose_db():
    """ Returns instance of Database"""
    try:
        chosen_db = int(input("Which database would you like to browse?\n"
                              "1 - TV series database.\n"
                              "2 - movie database.\n"))
        options = [1, 2]
        assert 0 < chosen_db < options[-1] + 1
        chosen_db = instantiate_db(chosen_db)
        return chosen_db
    except Exception:
        print("Wrong value entered. Please choose again.\n")
        return choose_db()


def instantiate_db(chosen_db):
    if chosen_db == 1:
        db = Database("tvseries_data")
        return db
    elif chosen_db == 2:
        db = Database("movies_data")
        return db


def choose_action():
    try:
        chosen_action = int(input("What would you like to do?\n"
                                  "1 - see whole database\n"
                                  "2 - see average evaluation for a title\n"
                                  "3 - see number of evaluations for a title\n"
                                  "4 - see all evaluations for a title\n"
                                  "5 - add new evaluation\n"))
        options = [1, 2, 3, 4, 5]
        assert 0 < chosen_action < options[-1] + 1
        return chosen_action
    except Exception:
        print("Wrong value entered. Please choose again.\n")
        return choose_action()


def do_action():
    chosen_db = choose_db()
    chosen_action = choose_action()
    if chosen_action == 1:
        print(chosen_db)
    elif chosen_action == 2:
        print_avg_evals(chosen_db)
    elif chosen_action == 3:
        print_cnt_evals(chosen_db)
    elif chosen_action == 4:
        print_get_evals(chosen_db)
    elif chosen_action == 5:
        evaluate(chosen_db)


def print_avg_evals(db):
    return print(db.avg_evals(input("Enter title: ")))


def print_cnt_evals(db):
    return print(db.cnt_evals(input("Enter title: ")))


def print_get_evals(db):
    return print(db.get_evals(input("Enter title: ")))


def evaluate(database):
    new_tit = ask_for_title()
    new_eval = ask_for_evaluation()
    database.insert_eval(new_tit, new_eval)
    print("Your evaluation: '{}': {} \nYour evaluation is much appreciated.".format(new_tit, new_eval))


def ask_for_title():
    new_title = input("Enter title: ")
    try:
        assert len(new_title) > 0
        return new_title
    except AssertionError:
        print("You have not given any title. Try again.\n".format(new_title))
        return ask_for_title()


def ask_for_evaluation():
    new_evaluation = input("Enter evaluation 1-10: ")
    try:
        assert 0 < int(new_evaluation) < 11
        return new_evaluation
    except Exception:
        print("Entered value ({}) outside the scope of possible options (1-10). Try again.\n".format(new_evaluation))
        return ask_for_evaluation()


def question():
    answ = input("\nWould you like to continue (y or n) ?\n")
    if answ == 'y':
        return True
    elif answ == 'n':
        return False
    else:
        print("\nWrong value entered. Please choose again.\n")
        return question()
