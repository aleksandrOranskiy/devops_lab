while True:
    try:
        number = int(input("Enter a number in range (1<= n <=99): "))
    except ValueError:
        print("Your number is incorrect, please enter it again: ")
        continue
    else:
        if any([number < 1, number > 99]):
            print("Your number is out of range, please enter it again: ")
            continue
        else:
            break

column_width = len(str(bin(number)))-2

for i in range(1, number + 1):
    print("{0:^{width}d}".format(i, width=column_width), end=' ')
    print("{0:^{width}o}".format(i, width=column_width), end=' ')
    print("{0:^{width}X}".format(i, width=column_width), end=' ')
    print("{0:^{width}b}".format(i, width=column_width))
