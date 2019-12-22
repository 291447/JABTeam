# -*- coding: utf-8 -*-
import arcpy
from classes import *

#Funkcja tworzaca graf
def create_graf(cursor):

	graf = Graf() #tworzenie obiektu klasy Graf
	for row in cursor:
		#pobranie kolejnej krawedzi i dwoch wierzcholkow
		edge = Edge()
		n_start = Node()
		n_end = Node()
		
		#dodanie geometrii do wierzcholkow
		for part in row[1]:
			n_start.x = part[0].X
			n_start.y = part[0].Y
			n_end.x = part[len(part)-1].X
			n_end.y = part[len(part)-1].Y
		
		#stworzenie identyfikatorow
		n_start.id = str(n_start.x)+','+str(n_start.y)
		n_end.id = str(n_end.x)+','+str(n_end.y)
		
		#przypisanie odpowiednich wartosci do krawedzi
		edge.fromNode = n_start
		edge.toNode = n_end
		edge.length = row[2]
		edge.cur_length = edge.length
		edge.count_velocity(row[3])
		edge.count_time_of_travel(edge.velocity, 'real')
		edge.id = str(row[0])
		
		#sprawdzenie, czy nastepne wierzcholki naleza juz do grafu, jesli nie - dodanie ich
		if n_start.id not in graf.node:
			graf.node[n_start.id] = n_start
		graf.node[n_start.id].edges.append(edge)

		if n_end.id not in graf.node:
			graf.node[n_end.id] = n_end
		graf.node[n_end.id].edges.append(edge)
		
		#dodanie krawedzi do grafu
		graf.edge[edge.id] = edge

	return graf