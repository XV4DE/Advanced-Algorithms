from sorts import *
import test

if __name__ == '__main__':
    my_list = [3, 1, 4, 1, 5, 9]
    insertion_sort(my_list)
    print(my_list)

    my_list = [3, 1, 4, 1, 5, 9]
    selection_sort(my_list)
    print(my_list)

    my_list = [3, 1, 4, 1, 5, 9]
    selection_sort(my_list)
    print(my_list)

    my_list = [1, 2,
               3, 4]
    my_list = transpose(my_list, 2)
    print(my_list)

    my_list = [1, 2,
               3, 4]
    my_list = column_sort(my_list, 2)
    print(my_list)
