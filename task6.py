whole_line = input("Please enter a string: ")
words_list = whole_line.split()
result_string = ""
counter = 0
for i in words_list:
    if counter != 0:
        result_string += " "
    result_string += i[::-1]
    counter += 1

print(result_string)
