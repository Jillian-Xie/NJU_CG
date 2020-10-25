line = [1, 2, 3, 4, 5, 6, 7]
p_list = [list(elem) for elem in list(zip(line[2: -1: 2], line[3:-1:2]))]
print(p_list)
