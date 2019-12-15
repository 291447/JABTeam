# -*- coding: utf-8 -*-
from classes import *
from fibonacciHeap import *
from heuristic import *

def get_closest(node, list_of_nodes):
	node2_x, node2_y = node.split(',')
	node2_x = float(node2_x)
	node2_y = float(node2_y)
	#print(node2_x, node2_y)
	minLen = 999999999999999
	for id, nd in list_of_nodes.items():
		node1_x = nd.x
		node1_y = nd.y
		len = heuristic_euc(node1_x, node1_y, node2_x, node2_y)
		if len < minLen:
			minLen = len
			node = nd
	return node

def A_star(graf, start, end, param):
	if (start or end not in graf.node):
		start = get_closest(start, graf.node)
		end = get_closest(end, graf.node)

	visited = set()
	visited.add(start.id)
	
	#cameFrom = {}                   #wierzcholki odwiedzone
	#cameFrom[start.id] = None
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
					g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.cur_time_of_travel
				else:
					g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.cur_length
				#cameFrom[nextEdge.toNode.id] = prevNode.id
				cameFrom_edge[nextEdge.id] = prevEdge
				
			else:
				prev_g = g_score[nextEdge.toNode.id]
				if param == 1:
					cur_g = g_score[prevNode.id] + nextEdge.cur_time_of_travel
				else:
					cur_g = g_score[prevNode.id] + nextEdge.cur_length
				if cur_g < prev_g:
					g_score[nextEdge.toNode.id] = cur_g
					#cameFrom[nextEdge.toNode.id] = prevNode.id
					cameFrom_edge[nextEdge.id] = prevEdge
				else:
					continue
					
			if nextEdge.id not in cameFrom_edge:
				for id, nEdge in cameFrom_edge.items():
					if nEdge == prevEdge:
						nodeid = graf.edge[id].toNode.id
						fromnodeid = graf.edge[id].fromNode.id
						if (nodeid == nextEdge.toNode.id and nextEdge.fromNode.id == fromnodeid):
							if ((param == 0 and nextEdge.cur_length > graf.edge[id].cur_length) or (param == 1 and nextEdge.cur_time_of_travel > graf.edge[id].cur_time_of_travel)):
								if_cypel = 1
								continue
				if if_cypel == 1:
					if_cypel = 0
					continue

			h = heuristic_euc(nextEdge.toNode.x, nextEdge.toNode.y, end.x, end.y)
			if param == 1:
				h = h/1000
			else:
				h = h/10
			f = g_score[nextEdge.toNode.id] + h
			
			y_key = (f, nextEdge.toNode.id, nextEdge.id)
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
		
		if fibHeap.count == 0:
			return 0
		min = fibHeap.extract_min()
		nodeid = min[1]
		edgeid = min[2]
		while (nodeid in visited):
			min = fibHeap.extract_min()
			nodeid = min[1]
			edgeid = min[2]
			pedge = edgeid
			if nodeid in added_to_fibHeap:
				added_to_fibHeap.remove(nodeid)
			prevmin = min[0]
		
		prevmin = min[0]
		pedge = edgeid
		prevEdge = edgeid
		prevNode = graf.node[nodeid]
		visited.add(prevNode.id)

	l = prevNode.id
	path = []
	'''
	while cameFrom[l] != None:
		nd = cameFrom[l]
		path.append(nd)
		l = nd
	'''
	
	k = prevEdge
	total = 0
	
	if param == 0:
		while cameFrom_edge[k] != None:
			ed = cameFrom_edge[k]
			total += graf.edge[ed].length
			path.append(ed)
			k = ed
		total += graf.edge[prevEdge].length
	else:
		while cameFrom_edge[k] != None:
			ed = cameFrom_edge[k]
			total += graf.edge[ed].time_of_travel
			path.append(ed)
			k = ed
		total += graf.edge[prevEdge].time_of_travel
	

	path.reverse()
	path.append(prevEdge)
	
	return (path, i, total)