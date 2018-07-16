def read_line(data):
    values = data.split()
    parsed_values = list(map(int, values))
    return parsed_values


def read_with_check(value):
    checked_values = list(filter(lambda x: 1 <= x <= 10 ** 9, value))
    if checked_values == value:
        return value
    else:
        return 1


def get_first_line(first_line):
    n, m = first_line[0], first_line[1]
    if any([n > 10 ** 5 + 1, n < 1, m > 10 ** 5 + 1, m < 1]):
        return 1
    else:
        return first_line


def get_result(first_list, list_1, list_2, m):
    array = read_with_check(first_list)

    other_arrays = []
    other_arrays.append(read_with_check(list_1))
    other_arrays.append(read_with_check(list_2))

    while True:
        if len(set(other_arrays[0] + other_arrays[1])) != m * 2:
            return 1
        else:
            break

    initial_happiness = 0
    for j in array:
        if j in other_arrays[0] and j not in other_arrays[1]:
            initial_happiness += 1
        elif j in other_arrays[1] and j not in other_arrays[0]:
            initial_happiness -= 1

    return "Resulting happiness is: {0}".format(initial_happiness)


def process():
    first_line = read_line("3 2")
    checked_first = get_first_line(first_line)
    second_line = read_line("1 5 3")
    checked_second = read_with_check(second_line)
    third_line = read_line("1 5")
    checked_third = read_with_check(third_line)
    fourth_line = read_line("2 4")
    checked_fourth = read_with_check(fourth_line)
    result = get_result(checked_second,
                        checked_third,
                        checked_fourth, checked_first[1])
    print(result)


process()
