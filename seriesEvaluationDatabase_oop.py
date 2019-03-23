# VERSION 2
# Creates small database with TV series titles and their evaluations.
# Enables user to retrieve data about series evaluation
# Enables user to add new series with evaluation
# TODO exceptions: floats as evaluation - convert
# TODO multiple evaluations for each TV series possible, use sth like Counter from statistics module for avg

series_eval_database = {"The Wire": 9,
                            "The Shield": 10,
                            "True Detective": 10,
                            "Battlestar Galactica": 8,
                            "The Expanse": 6,
                            "Twin Peaks": 8}

for ser, eval in series_eval_database.items():
    print(ser)


chooseSeries = input("\nEnter the title of the series to see evaluation:\n")
try:
    print("'{}' has the following evaluation: {}".format(chooseSeries, series_eval_database[chooseSeries]))
except KeyError:
    print("The title you entered is absent from the TV series database.\n"
          "Would you like to add a new evaluation for this TV series? (y/n)")
    answer = input()
    if answer == 'y':
        newSeriesTitle = chooseSeries
        newSeriesEvaluation = input("Add evaluation 1-10 for '{}': \n".format(newSeriesTitle))
        try:
            newSeriesEvaluation = int(newSeriesEvaluation)
        except ValueError:
            print("C'mon, no decimal points are needed for the scale of 1-10!")
            pass
        if 0 < newSeriesEvaluation < 11:
            series_eval_database[newSeriesTitle] = int(newSeriesEvaluation)
            print("Your evaluation has been added to the TV series database:\n", series_eval_database)
        else:
            print("Wrong value entered for evaluation")
    elif answer == 'no':
        pass
    else:
        print("Wrong key entered. You can try again.")
        pass

print("Would you like to add a new TV series with evaluation to the database? (y/n)")
answer = input()
if answer == 'y':
    newSeriesTitle = input("\nEnter the title of the new TV series.\n")
    newSeriesEvaluation = int(input("Add evaluation 1-10 for '{}': \n".format(newSeriesTitle)))
    if 0 < newSeriesEvaluation < 11:
        series_eval_database[newSeriesTitle] = int(newSeriesEvaluation)
        print("Your evaluation has been added to the TV series database:\n", series_eval_database)
    else:
        print("Wrong value entered for evaluation")
elif answer == 'no':
    pass
else:
    print("Wrong key entered. Program will end.")
    pass

