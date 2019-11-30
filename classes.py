# -*- coding: utf-8 -*-
class Graf:
	edge = []
	node = {}
	def print_graf(self):
		print('nodes: ')
		for key in self.node:
			self.node[key].print_node()
			
		print('edges: ')
		for i in range(0,len(self.edge)):
			self.edge[i].print_edge()
			
	#def find_node(self, id):
	#	return node[id]

class Node:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.h = 0
		self.id = 0
		self.edges = [] #sasiedzi
		self.f = 0
		self.final_cost = 0
	'''	
	def count_h(self):
		heuristic_euc_dist(node1_x, node1_y, node2_x, node2_y, Dist):
	'''
	def print_node(self):
		print('Node (id, x, y, h):')
		print(self.id, self.x, self.y, self.h)
		for i in range(0,len(self.edges)):
			self.edges[i].print_edge()
	
	'''	
	def check_if(self, other):
		is_in = 0
		for i in range(0,len(self.edges)):
			if self.edges[i].toNode == other:
				is_in = is_in + 1
		if is_in > 0:
			return 1
		else: return 0
	'''

class Edge:
	#IDENTYFIKATOR W RAZIE CZEGO
	fromNode = Node()
	toNode = Node()
	cost = 0.0
	length = 0
	velocity = 0
	
	def print_edge(self):
		print('From: ', self.fromNode.id, 'To: ', self.toNode.id, 'Cost: ',self.cost, 'Length: ',self.length)
		
class NodeQ:

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        return str(self.data)

class PriorityQueue:

    def __init__(self):
        self.head = None

    def is_empty(self):
        return not self.head

    def insert(self, data):
        node = NodeQ(data)
        before = None
        after = self.head
        while after:
            if after.data.f >= node.data.f: break
            before = after
            after = after.next
        if before is None:
            node.next = self.head
            self.head = node
        else:
            node.next = before.next
            before.next = node

    def remove(self):
        data = self.head.data
        self.head = self.head.next
        return data