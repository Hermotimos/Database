import datetime


def ask_yes_or_no(prompt):
    answer = input(prompt)
    if answer in ('y', 'n'):
        return answer
    else:
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
    except Exception:
        print("Your note ({}) outside the scope of possible evaluations (1-10).\nTry again :)\n".format(new_evaluation))
        return ask_evaluation()


def ask_date(prompt_message):
    date = input("{}\n".format(prompt_message))
    if not date:
        return date
    else:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Wrong value entered. Please choose again.\n")
            return ask_date(prompt_message)



