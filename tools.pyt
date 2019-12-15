import math
import arcpy
import numpy as np

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Toolbox"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [Tool]


class Tool(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "PathFinder"
		self.description = ""
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
	
		in_network = arcpy.Parameter(displayName="Input Features Network", name="in_network", datatype="GPFeatureLayer", parameterType="Required", direction="Input", enabled = True)
		in_network.filter.list = ["Polyline"]

		in_points = arcpy.Parameter(displayName="Input Features Points", name="in_points", datatype="GPFeatureLayer", parameterType="Required", direction="Input")
		in_points.filter.list = ["Point"]

		in_param = arcpy.Parameter(displayName="Choose parameter", name="in_param", datatype="GPBoolean", parameterType="Optional", direction="Input")
	
		out_path = arcpy.Parameter(displayName="Output Shortest Path", name="out_path", datatype="GPFeatureLayer", parameterType="Required", direction="Output")
		out_altpath = arcpy.Parameter(displayName="Output Alternative Shortest Path", name="out_altpath", datatype="GPFeatureLayer", parameterType="Required", direction="Output")
		
		parameters = [in_network, in_points, in_param, out_path, out_altpath]
		return parameters

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):

		class Graf:
			edge = {}
			node = {}

		class Node:
			def __init__(self):
				self.x = 0.0
				self.y = 0.0
				self.id = 0
				self.edges = [] #sasiedzi
				#self.final_cost = 0
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
			
			def count_time_of_travel(self, klasa):
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
				
			def count_actual_time_of_travel(self, vel):
				self.cur_time_of_travel = 3.6 * self.length / vel
				if param == 'real':
					self.time_of_travel = self.cur_time_of_travel
		
		class Tree:
			def __init__(self, key):
				self.key = key
				self.children = []
				self.degree = 0
			
			def append(self, deg):
				self.children.append(deg)
				self.degree = self.degree + 1
		   
		class FibonacciHeap:
			def __init__(self):
				self.trees = []
				self.least = None
				self.count = 0
						
			def get_min(self):
				if self.least == None:
					return None
				return self.least.key        
	  
			def insert(self, key):
				sprout = Tree(key)                                   
				self.trees.append(sprout)                            
				if (self.least is None or key < self.least.key):    
					self.least = sprout
				self.count = self.count + 1                       
				
			def extract_min(self):
				if self.least != None:
					sprig = self.least                        
					for child in sprig.children:                    
						self.trees.append(child)
						
					self.trees.remove(sprig)                        
					if len(self.trees) == 0:
						self.least = None
					else:
						self.least = self.trees[0]
					self.reorder()                           
					self.count = self.count - 1               
					
					return sprig.key
				return None
			
			def reorder(self):
				A = [None]*int(math.floor(math.frexp(self.count)[1])+1)
				while self.trees != []:
					x = self.trees[0]
					degree = x.degree
					self.trees.remove(x)
					while A[degree] is not None:
						y = A[degree]
						if x.key > y.key:
							temp = x
							x = y
							y = temp
						x.append(y)
						A[degree] = None
						degree = degree + 1
					A[degree] = x
					
				self.least = None
				for k in A:
					if k is not None:
						self.trees.append(k)
						if (self.least is None or k.key < self.least.key):
							self.least = k
							
		def create_graf(cursor):

			graf = Graf()
			
			for row in cursor:
				edge = Edge()
				n_start = Node()
				n_end = Node()
				
				#n_start.x = row.start_x
				#n_start.y = row.start_y
				for part in row[1]:
					n_start.x = part[0].X
					n_start.y = part[0].Y
					n_end.x = part[len(part)-1].X
					n_end.y = part[len(part)-1].Y
				n_start.id = str(n_start.x)+','+str(n_start.y)
				
				#n_end.x = row.end_x
				#n_end.y = row.end_y
				n_end.id = str(n_end.x)+','+str(n_end.y)
				
				edge.fromNode = n_start
				edge.toNode = n_end
				edge.length = row[2]
				edge.cur_length = edge.length
				edge.count_time_of_travel(row[3])
				edge.count_actual_time_of_travel(edge.velocity)
				edge.id = str(row[0])
				
				if n_start.id not in graf.node:
					graf.node[n_start.id] = n_start
				graf.node[n_start.id].edges.append(edge)

				if n_end.id not in graf.node:
					graf.node[n_end.id] = n_end
				graf.node[n_end.id].edges.append(edge)
				
				graf.edge[edge.id] = edge

			return graf	
			
		def heuristic_euc(node1_x, node1_y, node2_x, node2_y):
			dx = abs(node1_x - node2_x)
			dy = abs(node1_y - node2_y)
			if node1_x == node2_x and node1_y == node2_y:
				return 0
			return np.sqrt((dx)**2 + (dy)**2)
			
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
			
		def alt_path(prev_path, graf, param, start, end):
			if param == 1:
				for edge_id in prev_path:
					#print(graf.edge[edge_id].length)
					graf.edge[edge_id].alt_velocity = graf.edge[edge_id].velocity / 1.1
					#print(graf.edge[edge_id].alt_velocity, graf.edge[edge_id].velocity)
					graf.edge[edge_id].count_time_of_travel(graf.edge[edge_id].alt_velocity, 'alt')
			else:
				for edge_id in prev_path:
					graf.edge[edge_id].alt_length = graf.edge[edge_id].length * 1.05
					graf.edge[edge_id].cur_length = graf.edge[edge_id].alt_length
			path, i, total = A_star(graf, start, end, param)
			if path == prev_path:
				if param == 1:
					for edge_id in prev_path:
						#print(graf.edge[edge_id].length)
						graf.edge[edge_id].alt_velocity = graf.edge[edge_id].velocity / 1.3
						#print(graf.edge[edge_id].alt_velocity, graf.edge[edge_id].velocity)
						graf.edge[edge_id].count_time_of_travel(graf.edge[edge_id].alt_velocity, 'alt')
				else:
					for edge_id in prev_path:
						graf.edge[edge_id].alt_length = graf.edge[edge_id].length * 1.3
						graf.edge[edge_id].cur_length = graf.edge[edge_id].alt_length
			path, i, total = A_star(graf, start, end, param)
			if path == prev_path:
				return 0
			return path, i, total
		
		in_network = parameters[0].valueAsText
		cursor_network = arcpy.da.SearchCursor(in_network, ["OID@", "SHAPE@" ,"SHAPE@LENGTH", 'klasaDrogi'])

		graf = create_graf(cursor_network)

		in_points = parameters[1].valueAsText
		cursor_points =  arcpy.da.SearchCursor(in_points, ["SHAPE@X", "SHAPE@Y"])
		x = []
		y = []
		for row in cursor_points:
			xx = row[0]
			x.append(xx)
			yy = row[1]
			y.append(yy)

		start = str(x[0])+','+str(y[0])
		end = str(x[1])+','+str(y[1])

		param = parameters[2].value
		arcpy.AddMessage(param)
		arcpy.AddMessage(str(param))
		outcome = A_star(graf, start, end, param)
		if outcome == 0:
			arcpy.AddMessage('Path not found')
		else:
			path, i, total = outcome
			expression = ""
			for single in path:
				if single != path[len(path) - 1]:
					expression = expression + '"FID" = ' + single + " OR "
				else:
					expression = expression + '"FID" = ' + single

			arcpy.env.overwriteOutput = True
			out_path = parameters[3].valueAsText
			arcpy.Select_analysis(in_network, out_path, expression)

			if param == 1:
				total = total/60
				unit = 'min'
			else:
				unit = 'm'
			arcpy.AddMessage('Total for path: ' + str(total) + ' ' + str(unit))
			
			outcome = alt_path(path, graf, param, start, end)
			if outcome == 0:
				arcpy.AddMessage('Alternative path not found')
			else:
				alt_path, alt_i, total = outcome
				expression = ""
				for single in alt_path:
					if single != alt_path[len(alt_path) - 1]:
						expression = expression + '"FID" = ' + single + " OR "
					else:
						expression = expression + '"FID" = ' + single

				arcpy.env.overwriteOutput = True
				out_altpath = parameters[4].valueAsText
				arcpy.Select_analysis(in_network, out_altpath, expression)
				if param == 1:
					total = total/60
					
				arcpy.AddMessage('Total for altermative path: ' + str(total) + ' ' + str(unit))

		return out_path, out_altpath
