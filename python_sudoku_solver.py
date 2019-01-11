import numpy as np
from copy import deepcopy
n = 3
N = n * n
# Grid variable saves the final grid
Grid = []
Allowed = [[[1 for i in range(0, N)] for j in range(0, N)] for k in range(0, N)]

# print(Grid)

for i in range(0, N):
    s = input()
    s = s.split(sep=" ")
    row = []
    for j in range(0, N):
        row.append(int(s[j]))
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

# CSP Type Solution
#   Structure:
#       Grid to store solution
#       Allowed to store if allowed yet or not
#       
#   Functions:
#       is_allowed - simple check Allowed value
#       insert_num - inserts into pos and makes changes to Allowed
#       is_complete - simple check empty space in grid
#       is_valid_state - should have atleast one option available in each cell
#       next_cell - finds nect cell with minimum possible options to choose from
#       initialize_board - sets all given values
#       is_lonely - checks if it is the only possible value in a row column box
#       find_lonely_guys - fills up all the lonely places
#       solve_board - recursive function to solve the board


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
    Allowed[num, n*int(x/n):n*int(x/n)+n, n*int(y/n):n*int(y/n)+n] = Allowed[num, n*int(x/n):n*int(x/n)+n, n*int(y/n):n*int(y/n)+n] & 0
    Allowed[num, x, y] = 1


def is_complete():
    if -1 in Grid:
        return False
    else:
        return True


def is_final_valid_state():
    c1 = True
    state = [[0 for i in range(0, N)] for j in range(0, N)]
    state = np.asarray(state)
    for i in range(0, N):
        state = state | Allowed[i, :, :]
    if 0 in state:
        return False

    
    for j in range(0,n):
        for k in range(0,n):
            if not np.size(Grid[n*j:n*j+n, n*k:n*k+n]) == np.size(np.unique(Grid[n*j:n*j+n, n*k:n*k+n])):
                return False

    for j in range(0,N):
        if not np.size(Grid[j, :]) == np.size(np.unique(Grid[j, :])):
            return False 
        if not np.size(Grid[:, j]) == np.size(np.unique(Grid[:, j])):
            return False 
    
    return True

def is_valid_state():
    c1 = True
    state = [[0 for i in range(0, N)] for j in range(0, N)]
    state = np.asarray(state)
    for i in range(0, N):
        state = state | Allowed[i, :, :]
    if 0 in state:
        return False

    for j in range(0,n):
        for k in range(0,n):
            part = Grid[n*j:n*j+n, n*k:n*k+n]
            part = np.ndarray.flatten(part)
            part = part[part!=-1]
            if not np.size(part) == np.size(np.unique(part)):
                return False

    for j in range(0,N):
        part1 = Grid[j, :]
        part1 = np.ndarray.flatten(part1)
        part1 = part1[part1!=-1]
        part2 = Grid[:, j]
        part2 = np.ndarray.flatten(part2)
        part2 = part2[part2!=-1]
        if not np.size(part1) == np.size(np.unique(part1)):
            return False 
        if not np.size(part1) == np.size(np.unique(part1)):
            return False

    return True


def next_cell():
    state = [[0 for i in range(0, N)] for j in range(0, N)]
    state = np.asarray(state)
    for i in range(0, N):
        state = state + Allowed[i, :, :]
    state = state + (N+5) - (N+5) * (Grid == -1)
    index = np.unravel_index(np.argmin(state, axis=None), state.shape)
    return index


def initialize_board():
    for i in range(0, N):
        for j in range(0, N):
            if not Grid[i, j] == -1:
                insert_num(Grid[i, j], i, j)


def is_lonely(num, x, y):
    # print(Allowed[num, x, :])
    # print(Allowed[num, :, y])
    # print(Allowed[:, x, y])
    # print(Allowed[num, n*int(x/n):n*int(x/n)+n, n*int(y/n):n*int(y/n)+n])
    c1 = (Allowed[num, x, :] == 0).all()
    c2 = (Allowed[num, :, y] == 0).all()
    c3 = (Allowed[:, x, y] == 0).all()
    c4 = (Allowed[num, n*int(x/n):n*int(x/n)+n, n*int(y/n):n*int(y/n)+n] == 0).all()
    return c1 or c2 or c3 or c4


def find_lonely_guys():
    global Allowed
    for i in range(0, N):
        for j in range(0, N):
            for k in range(0, N):
                if Grid[j, k] == -1 and Allowed[i, j, k] == 1:
                    Allowed[i, j, k] = 0
                    if is_lonely(i, j, k):
                        # tempAllowed = deepcopy(Allowed)
                        insert_num(i, j, k)
                        # if not is_valid_state():
                        #     Allowed = deepcopy(tempAllowed)                            
                    Allowed[i, j, k] = 1


def solve_board():
    if is_complete() and is_final_valid_state():
        return True
    else:
        global Allowed
        if not is_valid_state():
            return False
        PrevAllowed = deepcopy(Allowed)
        # find_lonely_guys()
        PrevLonely = deepcopy(Allowed)
        (x_coor, y_coor) = next_cell()
        # print(str(x_coor) + " " + str(y_coor))
        for i in range(0, N):
            if is_allowed(i, x_coor, y_coor):
                insert_num(i, x_coor, y_coor)
                # print(Grid)
                # print("\n")
                if solve_board():
                    return True
                Grid[x_coor, y_coor] = -1
                Allowed = deepcopy(PrevLonely)
        Allowed = deepcopy(PrevAllowed)
        return False


initialize_board()

if solve_board():
    print(Grid+1)
else:
    print("Unsolved")


# Difficult sudoku
# 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 3 0 8 5
# 0 0 1 0 2 0 0 0 0
# 0 0 0 5 0 7 0 0 0
# 0 0 4 0 0 0 1 0 0
# 0 9 0 0 0 0 0 0 0
# 5 0 0 0 0 0 0 7 3
# 0 0 2 0 1 0 0 0 0
# 0 0 0 0 4 0 0 0 9


# Most Difficult Proclaimed
# 8 0 0 0 0 0 0 0 0
# 0 0 3 6 0 0 0 0 0
# 0 7 0 0 9 0 2 0 0
# 0 5 0 0 0 7 0 0 0
# 0 0 0 0 4 5 7 0 0
# 0 0 0 1 0 0 0 3 0
# 0 0 1 0 0 0 0 6 8
# 0 0 8 5 0 0 0 1 0
# 0 9 0 0 0 0 4 0 0

