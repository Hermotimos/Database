from communication import do_action, ask_continue


def main():
    while True:
        do_action()
        if not ask_continue():
            break


main()
