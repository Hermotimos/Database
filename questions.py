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
        print("Your note ({}) outside the scope of possible evaluations (1-10).\nTry again :)\n".format(new_evaluation))
        return ask_evaluation(prompt)


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
