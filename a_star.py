from classes import *
from fibonnaciHeap import *
#funkcje czekajace na implementacje
#def neighbours(node):
#    return set_of_node_neghbours
'''   
def reconstruct_path(came_from, currnt_node):
    if came_from is set:
        path = reconstruct_path(came_from)
            return path
'''
'''
def reconstruct_path(cameFrom, current)
    total_path = {currentNode}
    while currentNode in cameFrom.Keys:
        current := cameFrom[current]
        total_path.prepend(current)
    return total_path
    
def f_score(node):
    return g_score(node) + heuristic_estimation 
    
def g_score(node):
    #dlugosc krawedzi od startu do current_node
    
def heuristic_value(node):
    #
'''  
def A_star(graf, start, end):
	visited = set()
	visited.add(start)
	#cameFrom = {}                   #wierzcholki odwiedzone
	
	not_visited = FibonacciHeap()
	for edge in start.edges:
		not_visited.insert([edge.toNode.f, edge.toNode.id])
	g_score = {}                              #odleglosc od startu
	g_score[start.id] = 0
	nd = start
    
	while not_visited.count != 0:
		for y in nd.edges:
			if y.toNode in visited:
				continue
			if y.toNode.id not in g_score:
				g_score[y.toNode.id] = g_score[nd.id] + y.length
			else:
				prev_g = g_score[y.toNode.id]
				cur_g = g_score[nd.id] + y.length
				if cur_g < prev_g:
					g_score[y.toNode.id] = cur_g
			y.toNode.f = g_score[y.toNode.id] + y.toNode.h
			#anticipated_isbetter = false
			y_key = [y.toNode.f, y.toNode.id]
			if y_key not in not_visited: #ZAIMPLEMENTOWAC FUNKCJE W KOPCU!
				not_visited.insert([y.toNode.f, y.toNode.id])
				#h_score = heuristic_estimation(y, end)
				#anticipated_isbetter = true
			'''
			if g_score[y.toNode.id] < g_score(y):
				anticipated_isbetter = true
			'''
			#if anticipated_isbetter:
			
			x = not_visited.extract_min()
			print(x)
			#if x[1] == end.id:
				#return reconstruct_path(came_from, end)
			#not_visited.discard(x)
			nd = graf.node[x[1]]
			visited.add(nd)