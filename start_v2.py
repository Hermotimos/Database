from communication import do_action
from questions import ask_yes_or_no


def question():
    answ = ask_yes_or_no("\nWould you like to continue (y or n) ?\n")
    if answ == 'y':
        return True
    elif answ == 'n':
        return False


is_start = True
while is_start is True:
    do_action()
    is_start = question()
