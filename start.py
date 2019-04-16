"""
    This is the main module of the program.
"""
from communication import do_action, ask_continue


def main():
    while True:
        do_action()
        if not ask_continue("\nWould you like to continue (y/n) ?\n"):
            break


main()
