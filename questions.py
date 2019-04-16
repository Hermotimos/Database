"""
    Defines input functions for interaction with user.

    All functions in this module are exported to communication.py.
    All functions in this module call themselves recursively in case user enters value from outside choice options.

    ask_yes_or_no: Asks user for answer 'y' or 'n'.
    ask_title: Asks user to enter title (cannot be empty string).
    ask_evaluation: Asks user to evaluate title 1-10.
    ask_date: Asks user to enter date in yyyy-mm-dd format.
"""
import time


def ask_yes_or_no(prompt):
    answer = input(prompt)
    try:
        assert answer in ('y', 'n')
        return True if answer == 'y' else False
    except AssertionError:
        print("Wrong value entered. Please choose again.\n")
        return ask_yes_or_no(prompt)


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
    except (AssertionError, ValueError):
        print("Your note ({}) outside the scope of possible evaluations (1-10).\nTry again :)\n".format(new_evaluation))
        return ask_evaluation()


def ask_date(prompt_message):
    date = input("{}\n".format(prompt_message))
    if not date:
        return ''
    else:
        try:
            time.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Wrong value entered. Please choose again.\n")
            return ask_date(prompt_message)



