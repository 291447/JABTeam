# -*- coding: utf-8 -*-
import arcpy
from classes import *

def create_graf(cursor):

	graf = Graf()
	
	for row in cursor:
	
		edge = Edge()
		n_start = Node()
		n_end = Node()
		
		n_start.x = row.start_x
		n_start.y = row.start_y
		n_start.id = str(n_start.x)+','+str(n_start.y)
		
		n_end.x = row.end_x
		n_end.y = row.end_y
		n_end.id = str(n_end.x)+','+str(n_end.y)
		
		edge.fromNode = n_start
		edge.toNode = n_end
		edge.length = row.length
		edge.cur_length = edge.length
		edge.count_time_of_travel(row.klasaDrogi)
		edge.count_actual_time_of_travel(edge.velocity)
		edge.id = str(row.FID)
		
		if n_start.id not in graf.node:
			graf.node[n_start.id] = n_start
		graf.node[n_start.id].edges.append(edge)

		if n_end.id not in graf.node:
			graf.node[n_end.id] = n_end
		graf.node[n_end.id].edges.append(edge)
		
		graf.edge[edge.id] = edge
		
	return graf