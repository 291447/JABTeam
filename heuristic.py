import numpy as np 
	
def heuristic_euc(node1_x, node1_y, node2_x, node2_y):
	dx = abs(node1_x - node2_x)
	dy = abs(node1_y - node2_y)
	if node1_x == node2_x and node1_y == node2_y:
		return 0
	return np.sqrt((dx)**2 + (dy)**2)
