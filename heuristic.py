import numpy as np 

def heuristic_sr(node1_x, node1_y, node2_x, node2_y):
	return abs(node1_x - node2_x) + abs(node1_y - node2_y)
	
def heuristic_euc(node1_x, node1_y, node2_x, node2_y):
	D = 1
	D2 = np.sqrt(2)
	dx = abs(node1_x - node2_x)
	dy = abs(node1_y - node2_y)
	return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
	
node1_x = 12
node2_x = 130
node1_y = 1
node2_y = 5
	
heur = heuristic_euc(node1_x, node1_y, node2_x, node2_y)
print(heur)
	