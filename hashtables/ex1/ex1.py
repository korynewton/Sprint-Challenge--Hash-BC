#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize,
                        )


# input: weights = [ 4, 6, 10, 15, 16 ], length = 5, limit = 21
# output: [ 3, 1 ]  # since these are the indices of weights 15 and 6 whose sum equals 21


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for i in range(len(weights)):
        hash_table_insert(ht, weights[i], i)

    for i in range(len(weights)):
        # number we will be looking for in hashtable to complete a valid pair
        valid_pair = limit - weights[i]

        # searcch hash table for the value that would work
        does_exist = hash_table_retrieve(ht, valid_pair)

        if does_exist:
            print(does_exist, i)
            return (does_exist, i)
    return None


def print_answer(answer):
    if answer is None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")


get_indices_of_item_weights([4, 6, 10, 15, 16], 5, 21)
