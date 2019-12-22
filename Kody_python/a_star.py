# -*- coding: utf-8 -*-
from classes import *
from fibonacciHeap import *
from heuristic import *

#Funkcja odnajdujaca wezel najblizszy punktowi poczatkowemu oraz koncowemu
def get_closest(node, list_of_nodes):
	node2_x, node2_y = node.split(',')
	node2_x = float(node2_x)
	node2_y = float(node2_y)
	
	minLen = 9999999
	min = 0
	
	for id, nd in list_of_nodes.items():
		node1_x = nd.x
		node1_y = nd.y
		
		len = heuristic_euc(node1_x, node1_y, node2_x, node2_y)
		if len < minLen:
			min = 1
			minLen = len
			node = nd
			
	if min == 1:
		return node
		
	return 0

def A_star(graf, start, end, param):
	#Wybor wezla startowego oraz koncowego
	if (start or end not in graf.node):
		start = get_closest(start, graf.node)
		end = get_closest(end, graf.node)
		if start == 0 or end == 0:
			print("Point too far from network.")
			return 0
	
	visited = set() #zbior odwiedzonych wierzcholkow
	visited.add(start.id)
	
	cameFrom_edge = {} #slownik zawierajacy poprzedniki kolejnych krawedzi
	prevEdge = None #ustawienie poprzednika pierwszej krawedzi jako None
	
	fibHeap = FibonacciHeap() #kopiec Fibonacciego
	added_to_fibHeap = set()
	
	g_score = {} #odleglosc od startu
	g_score[start.id] = 0
	
	prevNode = start
	i = 0
	
	if_longest_way = 0

	while (prevNode.id != end.id):
		i = i + 1
		for nextEdge in prevNode.edges:
			#sprawdzenie, czy nalezy zamienic toNode z fromNode
			if nextEdge.toNode.id == prevNode.id:
				nextEdge.toNode, nextEdge.fromNode = nextEdge.fromNode, nextEdge.toNode
			
			#sprawdzenie czy nastepny wierzcholek byl juz odwiedzony
			if nextEdge.toNode.id in visited:
				continue
			
			if nextEdge.toNode.id not in g_score:
				if param == 1:
					g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.cur_time_of_travel
				else:
					g_score[nextEdge.toNode.id] = g_score[prevNode.id] + nextEdge.cur_length
				
				#jesli krawedz nie byla dodana do g_score, zostaje dodana do niego oraz do slownika poprzednikow
				cameFrom_edge[nextEdge.id] = prevEdge
				
			else:
				#jesli krawedz jest juz w g_score nastepuje porownanie poprzedniej wartosci z g_score z aktualna
				prev_g = g_score[nextEdge.toNode.id]
				if param == 1:
					cur_g = g_score[prevNode.id] + nextEdge.cur_time_of_travel
				else:
					cur_g = g_score[prevNode.id] + nextEdge.cur_length
				#podmiana poprzednikow, jesli sie okazuje, ze aktualna droga jest lepsza
				if cur_g < prev_g:
					g_score[nextEdge.toNode.id] = cur_g
					cameFrom_edge[nextEdge.id] = prevEdge
				else:
					continue
			
			#jesli funkcja przeszla wszystkie poprzednie warunki i krawedz dalej nie wystepuje w slowniku poprzednikow moze to oznaczac, ze wystepuja co najmniej
			#dwie krawedzie, ktore maja wspolne poczatki i konce
			if nextEdge.id not in cameFrom_edge:
				for id, nEdge in cameFrom_edge.items():
					if nEdge == prevEdge:
						nodeid = graf.edge[id].toNode.id
						fromnodeid = graf.edge[id].fromNode.id
						if (nodeid == nextEdge.toNode.id and nextEdge.fromNode.id == fromnodeid):
							if ((param == 0 and nextEdge.cur_length > graf.edge[id].cur_length) or (param == 1 and nextEdge.cur_time_of_travel > graf.edge[id].cur_time_of_travel)):
								if_longer_way = 1
								continue
				if if_longer_way == 1:
					if_longer_way = 0
					continue
			
			h = heuristic_euc(nextEdge.toNode.x, nextEdge.toNode.y, end.x, end.y) #obliczenie heurystyki
			#znormalizowanie heurystyki, aby rzad wielkosci byl podobny do porownywanych wartosci (odleglosci lub czasu)
			if param == 1:
				h = h/1000
			else:
				h = h/10
			
			#obliczenie wartosci f oraz dodanie odpowiednich wartosci do kopca Fibonacciego
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
		
		#jesli nie ma juz wartosci w kopcu Fibonacciego - droga nie istnieje
		if fibHeap.count == 0:
			return 0
		
		#pobranie najmniejszej wartosci z kopca
		min = fibHeap.extract_min()
		nodeid = min[1]
		edgeid = min[2]
		while (nodeid in visited):
			min = fibHeap.extract_min()
			nodeid = min[1]
			edgeid = min[2]
			if nodeid in added_to_fibHeap:
				added_to_fibHeap.remove(nodeid)
		
		#ustawienie wartosci poprzedniej krawedzi oraz poprzedniego wierzcholka i dodanie wierzcholka do zbioru z wierzcholkami odwiedzonymi
		prevEdge = edgeid
		prevNode = graf.node[nodeid]
		visited.add(prevNode.id)

	path = []
	k = prevEdge
	total = 0
	
	#tworzenie sciezki na podstawie slownika z poprzednikami
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