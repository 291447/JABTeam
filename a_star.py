# -*- coding: utf-8 -*-
from classes import *
from fibonacciHeap import *
from heuristic import *

def A_star(graf, start, end):
	visited = set()
	visited.add(start.id)
	
	cameFrom = {}                   #wierzcholki odwiedzone
	cameFrom[start.id] = None
	
	fibHeap = FibonacciHeap()
	added_to_fibHeap = set()
	
	g_score = {}                              #odleglosc od startu
	g_score[start.id] = 0
	
	prevNode = start
	i = 0

	while (prevNode.id != end.id):
		i = i + 1
		
		for nextEdge in prevNode.edges:
		
			if nextEdge.toNode.id == prevNode.id:
				nextEdge.toNode, nextEdge.fromNode = nextEdge.fromNode, nextEdge.toNode
			
			if nextEdge.toNode.id in visited:
				continue
			
			if nextEdge.toNode.id not in g_score:
				g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.length
				cameFrom[nextEdge.toNode.id] = prevNode.id
			else:
				prev_g = g_score[nextEdge.toNode.id]
				cur_g = g_score[prevNode.id] + nextEdge.length
				if cur_g < prev_g:
					g_score[nextEdge.toNode.id] = cur_g
					cameFrom[nextEdge.toNode.id] = prevNode.id
			
			h = heuristic_euc(nextEdge.toNode.x, nextEdge.toNode.y, end.x, end.y)
			f = g_score[nextEdge.toNode.id] + h
			
			y_key = (f, nextEdge.toNode.id)
			if y_key[1] not in added_to_fibHeap:
				fibHeap.insert(y_key)
				added_to_fibHeap.add(y_key[1])
			else:
				minim = fibHeap.get_min()
				if minim[1] == y_key[1]:
					if minim[0] > y_key[0]:
						fibHeap.extract_min()
						fibHeap.insert(y_key)
				else:
					fibHeap.insert(y_key)
					
		nodeid = fibHeap.extract_min()[1]
		while (nodeid in visited):
			nodeid = fibHeap.extract_min()[1]
			if nodeid in added_to_fibHeap:
				added_to_fibHeap.remove(nodeid)

		prevNode = graf.node[nodeid]
		visited.add(prevNode.id)

	l = prevNode.id
	path = []
	
	while cameFrom[l] != None:
		nd = cameFrom[l]
		path.append(nd)
		l = nd

	path.reverse()
	path.append(prevNode.id)
	
	return (path, i)