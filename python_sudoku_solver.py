import numpy as np
from copy import deepcopy
# Grid variable saves the final grid
Grid = []
Allowed = [[[1 for i in range(0, 9)] for j in range(0, 9)] for k in range(0, 9)]

# print(Grid)

for i in range(0, 9):
    s = input()
    s = s.split(sep=" ")
    row = []
    for j in s[:]:
        row.append(int(j))
    Grid.append(row)

# print(Grid)
# 0 0 0 6 0 4 7 0 0
# 7 0 6 0 0 0 0 0 9
# 0 0 0 0 0 5 0 8 0
# 0 7 0 0 2 0 0 9 3
# 8 0 0 0 0 0 0 0 5
# 4 3 0 0 1 0 0 7 0
# 0 5 0 2 0 0 0 0 0
# 3 0 0 0 0 0 2 0 8
# 0 0 2 3 0 1 0 0 0

# Functions needed:
#   check allowed- number , coordinate
#   insert number- number , coordinate
#   remove Allowed- number , coordinate
#   add Allowed- number , coordinate
#   solve board recursive fn- Grid
#   sort cell coordinates acc to ease of solving-
#   remove number- coordinate
#   find box- coordinate
#   find possibilities- to initially calculate possibilities for the whole grid and sort the coordinate list

# Structure needed
#   Dict key:coordinate value:List having allowed values
#   Grid: 9*9 stores result and used for checking allowed
#   List of coordinates - arranged in increasing order of number of possibilities

Grid = np.asarray(Grid, dtype=int)
Grid = Grid - 1
Allowed = np.asarray(Allowed, dtype=int)


def is_allowed(num, x, y):
    if Allowed[num, x, y] == 1:
        return True
    else:
        return False


def insert_num(num, x, y):
    Grid[x, y] = num
    Allowed[num, x, :] = Allowed[num, x, :] & 0
    Allowed[num, :, y] = Allowed[num, :, y] & 0
    Allowed[:, x, y] = Allowed[:, x, y] & 0
    Allowed[num, 3*int(x/3):3*int(x/3)+3, 3*int(y/3):3*int(y/3)+3] = Allowed[num, 3*int(x/3):3*int(x/3)+3, 3*int(y/3):3*int(y/3)+3] & 0
    Allowed[num, x, y] = 1


def is_complete():
    if -1 in Grid:
        return False
    else:
        return True


def is_valid_state():
    state = [[0 for i in range(0, 9)] for j in range(0, 9)]
    state = np.asarray(state)
    for i in range(0, 9):
        state = state | Allowed[i, :, :]
    if 0 in state:
        return False
    else:
        return True


# Find next solvable cell -
def next_cell():
    state = [[0 for i in range(0, 9)] for j in range(0, 9)]
    state = np.asarray(state)
    for i in range(0, 9):
        state = state + Allowed[i, :, :]
    state = state + 10 - 10 * (Grid == -1)
    index = np.unravel_index(np.argmin(state, axis=None), state.shape)
    return index


# Initialize the board - ok
def initialize_board():
    for i in range(0, 9):
        for j in range(0, 9):
            if not Grid[i, j] == -1:
                insert_num(Grid[i, j], i, j)


def solve_board():
    if is_complete():
        return True
    else:
        global Allowed
        if not is_valid_state():
            return False
        PrevAllowed = deepcopy(Allowed)
        (x_coor, y_coor) = next_cell()
        # print(str(x_coor) + " " + str(y_coor))
        for i in range(0, 9):
            if is_allowed(i, x_coor, y_coor):
                insert_num(i, x_coor, y_coor)
                # print(Grid)
                # print("\n")
                if solve_board():
                    return True
                Grid[x_coor, y_coor] = -1
                Allowed = deepcopy(PrevAllowed)
        return False


def is_lonely(num, x, y):
    # print(Allowed[num, x, :])
    # print(Allowed[num, :, y])
    # print(Allowed[:, x, y])
    # print(Allowed[num, (y % 3):(y % 3 + 3), (x % 3):(x % 3 + 3)])
    c1 = (Allowed[num, x, :] == 0).all()
    c2 = (Allowed[num, :, y] == 0).all()
    c3 = (Allowed[:, x, y] == 0).all()
    c4 = (Allowed[num, 3*int(x/3):3*int(x/3)+3, 3*int(y/3):3*int(y/3)+3] == 0).all()
    return c1 or c2 or c3 or c4


def find_lonely_guys():
    for i in range(0, 9):
        for j in range(0, 9):
            for k in range(0, 9):
                if Grid[j, k] == -1:
                    Allowed[i, j, k] = 0
                    if is_lonely(i, j, k):
                        insert_num(i, j, k)
                    Allowed[i, j, k] = 1


initialize_board()
find_lonely_guys()
print(Grid+1)

# if solve_board():
#     print(Grid+1)
# else:
#     print("Unsolved")
