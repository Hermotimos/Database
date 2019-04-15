from communication import do_action, continue_browsing

while True:
    do_action()
    if not continue_browsing():
        break
