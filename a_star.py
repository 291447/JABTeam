# -*- coding: utf-8 -*-
from classes import *
from fibonacciHeap import *
from heuristic import *

def A_star(graf, start, end):
	visited = set()
	visited.add(start)
	cameFrom = {}                   #wierzcholki odwiedzone
	cameFrom[start.id] = None
	added_to_not_visited = set()
	
	not_visited = FibonacciHeap()
	g_score = {}                              #odleglosc od startu
	g_score[start.id] = 0
	nd = start
	i = 0

	while (nd.id != end.id):
		i = i + 1
		for y in nd.edges:
			if y.toNode.id == nd.id:
				n = Node()
				n = y.toNode
				y.toNode = y.fromNode
				y.fromNode = n
			if y.toNode.id in visited:
				continue
			if y.toNode.id not in g_score:
				g_score[y.toNode.id] = g_score[nd.id] + y.length
				cameFrom[y.toNode.id] = nd.id
			else:
				prev_g = g_score[y.toNode.id]
				cur_g = g_score[nd.id] + y.length
				if cur_g < prev_g:
					g_score[y.toNode.id] = cur_g
					cameFrom[y.toNode.id] = nd.id
			y.toNode.h = heuristic_euc(y.toNode.x, y.toNode.y, end.x, end.y)
			y.toNode.f = g_score[y.toNode.id] + y.toNode.h
			y_key = [y.toNode.f, y.toNode.id]
			#not_visited.reorder()
			if y_key[1] not in added_to_not_visited:
				not_visited.insert(y_key)
				added_to_not_visited.add(y_key[1])
			else:
				minim = not_visited.get_min()
				if minim[1] == y_key[1]:
					if minim[0] > y_key[0]:
						not_visited.extract_min()
						not_visited.insert(y_key)
				else:
					not_visited.insert(y_key)
					added_to_not_visited.add(y_key[1])
		x = not_visited.extract_min()
		if x[1] in added_to_not_visited:
			added_to_not_visited.remove(x[1])
		nd = graf.node[x[1]]
		visited.add(nd.id)
	l = nd.id
	path = []
	while cameFrom[l] != None:
		prevNode = cameFrom[l]
		#final_cost = final_cost + prevNode.final_cost
		#print(final_cost)
		path.append(prevNode)
		l = prevNode
	path.reverse()
	path.append(nd.id)
	print(path, "liczba iter: ", i, "dlugosc sciezki: ", len(path))