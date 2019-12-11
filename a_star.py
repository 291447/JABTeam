# -*- coding: utf-8 -*-
from classes import *
from fibonacciHeap import *
from heuristic import *

def A_star(graf, start, end, param):
	visited = set()
	visited.add(start.id)
	
	cameFrom = {}                   #wierzcholki odwiedzone
	cameFrom[start.id] = None
	cameFrom_edge = {}
	prevEdge = None
	
	fibHeap = FibonacciHeap()
	added_to_fibHeap = set()
	
	g_score = {}                              #odleglosc od startu
	g_score[start.id] = 0
	
	prevNode = start
	i = 0
	
	if_cypel = 0
	prevmin = -1

	while (prevNode.id != end.id):
		i = i + 1
		
		for nextEdge in prevNode.edges:
			
			if nextEdge.toNode.id == prevNode.id:
				nextEdge.toNode, nextEdge.fromNode = nextEdge.fromNode, nextEdge.toNode
			
			if nextEdge.toNode.id in visited:
				continue
			
			if nextEdge.toNode.id not in g_score:
				if param == 1:
					g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.time_of_travel
				else:
					g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.cur_length
				if (nextEdge.id == '11668' or nextEdge.id == '9882'):
					print ('jeny', nextEdge.id, nextEdge.cur_length, g_score[nextEdge.toNode.id])
				cameFrom[nextEdge.toNode.id] = prevNode.id
				cameFrom_edge[nextEdge.id] = prevEdge
			else:
				prev_g = g_score[nextEdge.toNode.id]
				if param == 1:
					cur_g = g_score[prevNode.id] + nextEdge.time_of_travel
				else:
					if (nextEdge.id == '11668' or nextEdge.id == '9882'):
						print (nextEdge.id, nextEdge.cur_length)
					cur_g = g_score[prevNode.id] + nextEdge.cur_length
				if cur_g < prev_g:
					g_score[nextEdge.toNode.id] = cur_g
					cameFrom[nextEdge.toNode.id] = prevNode.id
					cameFrom_edge[nextEdge.id] = prevEdge
					if (nextEdge.id == '11668' or nextEdge.id == '9882'):
						print ('chyba nie', nextEdge.id, g_score[nextEdge.toNode.id], prevNode.id, prevEdge)
				
			if nextEdge.id not in cameFrom_edge:
				cameFrom_edge[nextEdge.id] = prevEdge
				if (nextEdge.id == '11668' or nextEdge.id == '9882'):
					print ('co', nextEdge.id, g_score[nextEdge.toNode.id], prevNode.id, prevEdge)
				#print (nextEdge.id)
			
			h = heuristic_euc(nextEdge.toNode.x, nextEdge.toNode.y, end.x, end.y)/1000
			f = g_score[nextEdge.toNode.id] + h
			###################################
			if (nextEdge.id == '11668' or nextEdge.id == '9882'):
				print (nextEdge.id, f, g_score[nextEdge.toNode.id], h, nextEdge.cur_length)
			#################################
			
			y_key = (f, nextEdge.toNode.id, nextEdge.id)
			#y_key = (f, nextEdge.toNode.id)
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
					
		min = fibHeap.extract_min()
		nodeid = min[1]
		edgeid = min[2]
		while (nodeid in visited):
			if prevmin == min[0] and pedge != edgeid:
				if graf.edge[edgeid].cur_length < graf.edge[pedge].cur_length:
					if edgeid == '11668' or edgeid == '9882':
						print('alert', pedge, edgeid)
						if_cypel = 1
						for id, nextEdge in cameFrom_edge.items():
							if nextEdge == pedge:
								cameFrom_edge[nextEdge] = edgeid
			min = fibHeap.extract_min()
			nodeid = min[1]
			edgeid = min[2]
			pedge = edgeid
			if nodeid in added_to_fibHeap:
				added_to_fibHeap.remove(nodeid)
			prevmin = min[0]
		
		prevmin = min[0]
		pedge = edgeid
		#cameFrom_edge[edgeid] = prevEdge
		prevEdge = edgeid
		prevNode = graf.node[nodeid]
		visited.add(prevNode.id)

	l = prevNode.id
	path = []
	path_edge = []
	
	while cameFrom[l] != None:
		nd = cameFrom[l]
		path.append(nd)
		l = nd

	k = prevEdge
	while cameFrom_edge[k] != None:
		ed = cameFrom_edge[k]
		path_edge.append(ed)
		k = ed
		
	path.reverse()
	path_edge.reverse()
	path.append(prevNode.id)
	path_edge.append(prevEdge)
	
	return (path, i, path_edge)