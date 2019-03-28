from communication import do_action


def question():
    answ = input("\nWould you like to continue (y or n) ?\n")
    if answ == 'y':
        return True
    elif answ == 'n':
        return False
    else:
        print("\nWrong value entered. Please choose again.\n")
        return question()


is_start = True
while is_start is True:
    do_action()
    is_start = question()
