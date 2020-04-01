import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--infile", type=str)
parser.add_argument("--outfile", type=str)
args = parser.parse_args()

""" Globals """
size = None
rootsize = None
squares = None
unitlist = None
units = None
peers = None

""" Functions """

## Utilities
def cross(A, B):
	" Cross Product of Elements in A and B "
	return [(a, b) for a in A for b in B]

def decode(s, typename=str):
	" Returns List of Set Bits in  String s "
	assert(len(s) == size)
	return [typename(i+1) for i in range(size) if s[i]=='1']

def some(seq): # first non False element in seq
	for e in seq:
		if e: return e
	return False

def parse_grid(grid_input):
	" Assign Initial Values to the grid and propagate "
	values = dict((s, "1"*size) for s in squares)
	for s, d in get_grid_dict(grid_input).items():
		if not d == 0 and not assign(values, s, d):
			return False
	return values

def get_grid_dict(grid_input):
	" Convert 2D int grid to dict of square -> int , 0 for empty "
	return dict(zip(squares, sum(grid_input, [])))

def assign(values, s, d):
	" Eliminate all values except d from square s in values, also propagate \
	any changes that occur "
	if not all(eliminate(values, s, o) for o in range(1,size+1) if o!=d):
		return False
	return values

def eliminate(values, s, d):
	" Eliminate the value d from square s in values, also propagate \
	any changes that occur "
	if values[s][d-1] == '0':
		return values

	values[s] = values[s][:d-1] + '0' + values[s][d:]
	if values[s] == '0'*size:
		return False ## No value possible in square s

	if values[s].count('1') == 1:
		d2 = values[s].find('1')
		if not all(eliminate(values, s2, d2+1) for s2 in peers[s]):
			return False
		
	for u in units[s]:
		dplaces = [s for s in u if values[s][d-1] == '1']
		if len(dplaces) == 0:
			return False ## No place to put d in row/column/box

		if len(dplaces) == 1:
			if not assign(values, dplaces[0], d):
				return False ## werent able to assign d to the only place possible

	return values

def display(values, **kwargs):
	width = 1+max(len(','.join(decode(values[s]))) for s in squares)
	line = '+'.join(['-'*(width*rootsize)]*rootsize)
	for i in range(1,size+1):
		x = [','.join(decode(values[(i, j)]))+(' |' if j % rootsize == 0 else '') for j in range(1,size+1)]
		print(''.join(xi.center(width) for xi in x), **kwargs)
		if i % rootsize == 0:
			print(line, **kwargs)

def search(values):
	" Depth First Search Recursively assigns values "
	if values is False:
		return False ## failed earlier
	if all(values[s].count('1') == 1 for s in squares):
		return values
	## Choose square with minimum possibilities
	_, s = min((values[s].count('1'), s) for s in squares if values[s].count('1') > 1)
	return some(search(assign(values.copy(), s, d)) for d in random.shuffle(decode(values[s], typename=int)))

def solve(grid_input):
	" Solve the grid input puzzle "
	return search(parse_grid(grid_input))


""" Setup variables and solve the Sudoku """
with open(args.infile, 'r') as infile:
	grid_input = [list(map(lambda x : int(x), l.strip().split(' '))) for l in infile.readlines() if l.strip() != '']

size = len(grid_input)
assert(size == len(grid_input[0]))

rootsize = int(size**(1/2))
assert(size == rootsize**2)

squares = cross(range(1, size+1), range(1, size+1))

unitlist = ([cross(range(1, size+1), [i]) for i in range(1, size+1)]
		  + [cross([i], range(1, size+1)) for i in range(1, size+1)]
		  + [cross(range(i*rootsize+1, i*rootsize+rootsize+1), 
		  		   range(j*rootsize+1, j*rootsize+rootsize+1)) 
		  		for i in range(0, rootsize) for j in range(0, rootsize)])

units = dict((s, [u for u in unitlist if s in u])
			 for s in squares)

peers = dict((s, set(sum(units[s], []))-set([s]))
			 for s in squares)

values = solve(grid_input)

if values:
	if args.outfile:
		with open(args.outfile, 'w') as outfile:
			display(values, file=outfile)
	else:
		display(values)
else:
	if args.outfile:
		with open(args.outfile, 'w') as outfile:
			print("UNSOLVED", file=outfile)
	else:
		print("UNSOLVED")