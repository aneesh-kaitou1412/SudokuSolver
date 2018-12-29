# Grid variable saves the final grid
Grid = []
# print(Grid)

for i in range(0, 9):
    s = input()
    s = s.split(sep=" ")
    row = []
    for j in s[:]:
        row.append(int(j))
    Grid.append(row)

# print(Grid)
# 1 2 3 4 5 6 7 8 9
# 2 3 4 5 6 7 8 9 1
# 3 4 5 6 7 8 9 1 2
# 4 5 6 7 8 9 1 2 3
# 5 6 7 8 9 1 2 3 4
# 6 7 8 9 1 2 3 4 5
# 7 8 9 1 2 3 4 5 6
# 8 9 1 2 3 4 5 6 7
# 9 1 2 3 4 5 6 7 8

