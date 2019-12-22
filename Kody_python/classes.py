# -*- coding: utf-8 -*-

#plik zawierajacy klasy Graf, Node oraz Edge

class Graf:

	edge = {}
	node = {}
	
	def print_graf(self):
		print('nodes: ')
		for key in self.node:
			self.node[key].print_node()
			
		print('edges: ')
		for i in range(0,len(self.edge)):
			self.edge[i].print_edge()

			
class Node:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.id = 0
		self.edges = [] #sasiedzi

	def print_node(self):
		print('Node (id, x, y, h):')
		print(self.id, self.x, self.y, self.h)
		for i in range(0,len(self.edges)):
			self.edges[i].print_edge()

			
class Edge:
	id = -1
	fromNode = Node()
	toNode = Node()
	cost = 0.0
	length = 0.0
	cur_length = 0.0
	velocity = 0.0
	time_of_travel = 0.0
	cur_time_of_travel = 0.0
	alt_velocity = 0.0
	alt_length = 0.0
	
	def count_velocity(self, klasa):
		if klasa == 'A':
			self.velocity = 120
		elif klasa == 'S':
			self.velocity = 90
		elif klasa == 'GP':
			self.velocity = 80
		elif klasa == 'G':
			self.velocity = 60
		elif klasa == 'Z':
			self.velocity = 50
		elif klasa == 'L':
			self.velocity = 20
		elif klasa == 'I':
			self.velocity = 10
		elif klasa == 'D':
			self.velocity = 10
		else:
			self.velocity = 50
		
	def count_time_of_travel(self, vel, param):
		#param = 'real' - mamy obliczyć właściwy czas
		#param = 'alt' - mamy obliczyć zmieniony czas
		self.cur_time_of_travel = 3.6 * self.length / vel
		if param == 'real':
			self.time_of_travel = self.cur_time_of_travel
	
	def print_edge(self):
		print('From: ', self.fromNode.id, 'To: ', self.toNode.id, 'Cost: ',self.cost, 'Length: ',self.length)