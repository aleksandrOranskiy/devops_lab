def parse_file(filename):
    result_list = []
    try:
        with open(filename) as f:
            try:
                first_line = f.readline()
                main_values = list(map(int, first_line.split()))

                # receiving and checking values of w and h
                w, h = main_values[0], main_values[1]
                if any([w < 1, h > 100]):
                    print("Parameters should be (1 ≤ w, h ≤ 100)!")
                    return 1
                else:
                    result_list.append(main_values)

                # receiving and checking a value of n
                n = int(f.readline())
                if any([n < 0, n > 5000]):
                    print("The parameter n should be (0 ≤ n ≤ 5000)!")
                    return 1
                else:
                    result_list.append(n)

                # receiving and checking coordinate values
                for i in range(n):
                    values = list(map(int, f.readline().split()))
                    filt_values = list(filter(lambda x: x >= 0, values))
                    if values != filt_values:
                        print("An issue with some of coordinates!")
                        return 1
                    else:
                        result_list.append(filt_values)

            except ValueError:
                print("Numbers in lines aren't correct!")
                return 1

    except IOError:
        print("File doesn't exist")

    return result_list


def write_file(filename, value):
    try:
        with open(filename, 'w') as o:
            o.write(value)
    except IOError:
        print("File doesn't exist")


parameters = parse_file('input.txt')

if parameters != 1:
    width, height = parameters[0][0], parameters[0][1]
    number = parameters[1]
    filled_square = 0

    # creating an array and filling it with zero
    whole_array = [[0 for j in range(width)] for i in range(height)]

    # filling the array with 1 where there is a square
    try:
        for j in range(2, number + 2):
            x1 = parameters[j][0]
            y1 = parameters[j][1]
            x2 = parameters[j][2]
            y2 = parameters[j][3]
            for h in range(x1, x2):
                for v in range(y1, y2):
                    whole_array[h][v] = 1

        all_square = width * height

        for k in range(height):
            filled_square += sum(whole_array[k])

        free_square = all_square - filled_square
        write_file('output.txt', str(free_square))
    except IndexError:
        print("An issue with parameters in the input file!")
