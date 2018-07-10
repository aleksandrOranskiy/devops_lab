while True:
    try:
        number = int(input("Enter a number in range (1-20): "))
    except ValueError:
        print("Your number is incorrect, please enter it again: ")
        continue
    else:
        if any([number < 0, number > 20]):
            print("Your number is out of range, please enter it again: ")
            continue
        else:
            break

for i in range(number):
    print(i ** 2)
