from communication import do_action
from questions import ask_if_continue

while True:
    do_action()
    if not ask_if_continue():
        break
