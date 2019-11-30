import numpy as np 

def heuristic_sr(node1_x, node1_y, node2_x, node2_y):
	return abs(node1_x - node2_x) + abs(node1_y - node2_y)
	
def heuristic_euc(node1_x, node1_y, node2_x, node2_y):
	dx = abs(node1_x - node2_x)
	dy = abs(node1_y - node2_y)
	if node1_x == node2_x and node1_y == node2_y:
		return 0
	return np.sqrt((dx)**2 + (dy)**2)
	
def heuristic_euc_dist(node1_x, node1_y, node2_x, node2_y, Dist):
	D2 =  Dist * np.sqrt(2)
	dx = abs(node1_x - node2_x)
	dy = abs(node1_y - node2_y)
	return Dist * (dx + dy) + (D2 - 2 * Dist) * min(dx, dy)

'''
#sprawdzenie	
node1_x = 12.124
node2_x = 13.4687
node1_y = 1.7529
node2_y = 5.3749
	
heur = heuristic_euc(node1_x, node1_y, node2_x, node2_y)
heur_sr = heuristic_sr(node1_x, node1_y, node2_x, node2_y)
Dist = 1
heuristic_euc1(node1_x, node1_y, node2_x, node2_y, Dist)
print(heur, heur_sr)
'''