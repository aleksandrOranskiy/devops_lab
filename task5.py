def read_line():
    while True:
        try:
            values = input().split()
            parsed_values = list(map(int, values))
            return parsed_values
        except ValueError:
            print("Some of numbers are incorrect, please enter it again: ")
            continue


def read_with_check(value):
    while True:
        curr_line = read_line()
        checked_values = list(filter(lambda x: 1 <= x <= 10 ** 9, curr_line))
        if len(curr_line) != value or curr_line != checked_values:
            print("Numbers should be in (1-10**9) or not correct amount of it")
            continue
        return curr_line


print("Enter numbers separated by a space:")
while True:
    first_line = read_line()
    n, m = first_line[0], first_line[1]
    if 10 ** 5 + 1 < n < 1 or 10 ** 5 + 1 < m < 1:
        print("Numbers n and m should be in the range (1-100000)")
        continue
    break

array = read_with_check(n)

other_arrays = []
for i in range(2):
    other_arrays.append(read_with_check(m))

while True:
    if len(set(other_arrays[0] + other_arrays[1])) != m * 2:
        print("Sets are intersected, enter the second again")
        other_arrays[1] = read_with_check(m)
    break

initial_happiness = 0
for j in array:
    if j in other_arrays[0] and j not in other_arrays[1]:
        initial_happiness += 1
    elif j in other_arrays[1] and j not in other_arrays[0]:
        initial_happiness -= 1

print("Resulting happiness is: {0}".format(initial_happiness))
