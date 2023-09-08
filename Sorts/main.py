from sorts import *
import test

if __name__ == '__main__':
    passes = 0
    attempts = 0

    attempts += 1
    if test.test_sort(insertion_sort):
        passes += 1

    attempts += 1
    if test.test_sort(selection_sort):
        passes += 1

    attempts += 1
    if test.test_transpose(transpose):
        passes += 1

    attempts += 1
    if test.test_greatest(greatest):
        passes += 1

    attempts += 1
    if test.test_column(column_sort):
        passes += 1


    print("Passed " + str(passes) + " of " + str(attempts) + " tests.")

    print("Insertion sort")
    for time in test.sorting_time_efficiency(insertion_sort):
        print(time)

    print()
    print()
    print()
    print("Selection sort")
    for time in test.sorting_time_efficiency(selection_sort):
        print(time)