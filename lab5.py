import arcpy
from classes import *
from a_star import *
from heuristic import *

arcpy.env.workspace = "C:\\3rok\\sem5\\PAG2\\pag"
'''
for fc in arcpy.ListFeatureClasses():
	print("{0},{1}".format(fc,arcpy.GetCount_management(fc)))
'''
in_features = "jezdnie_nasze.shp"

cursor = arcpy.SearchCursor(in_features)

g = Graf()
for row in cursor:
	e = Edge()
	e.length = row.length
	n_start = Node()
	n_end = Node()
	n_start.x = int(round(row.start_x))
	n_start.y = int(round(row.start_y))
	n_start.id = str(n_start.x)+','+str(n_start.y)
	n_end.x = int(round(row.end_x))
	n_end.y = int(round(row.end_y))
	n_end.id = str(n_end.x)+','+str(n_end.y)
	e.fromNode = n_start
	e.toNode = n_end
	g.edge.append(e)
	if n_start.id not in g.node:
		g.node[n_start.id] = n_start
	g.node[n_start.id].edges.append(e)
	if n_end.id not in g.node:
		g.node[n_end.id] = n_end
	g.node[n_end.id].edges.append(e)
	
'''	
for i in range(0,len(g.edge)):
	#g.edge[i].fromNode.print_node()
	#g.edge[i].toNode.print_node()
	g.node[str(g.edge[i].fromNode.x)+','+str(g.edge[i].fromNode.y)].print_node()
'''
A_star(g, g.node[str(g.edge[0].fromNode.x)+','+str(g.edge[0].fromNode.y)], g.node[str(g.edge[4].fromNode.x)+','+str(g.edge[4].fromNode.y)])

print('end')
'''
arcpy.AddField_management(in_features, 'start_x', 'double')
arcpy.CalculateField_management(in_features, 'start_x', '!shape.area!')
cursor = arcpy.SearchCursor("L4_1_BDOT10k__OT_SKJZ_L.shp")



arcpy.FeatureVerticesToPoints_management(in_features,
                                         "G:\\Asz\\kujawsko_pomorskie_m_Torun\\nodes", 
                                         "BOTH_ENDS")

arcpy.DeleteIdentical_management("G:\\Asz\\kujawsko_pomorskie_m_Torun\\nodes.shp", "Shape")

for row in cursor:
	print(row.x_kod, row.start_x)
infc = arcpy.GetParameterAsText(0)
for row in arcpy.da.SearchCursor(infc, ["SHAPE@XY"]):
	x, y = row[0]
	print("{}, {}".format(x, y))
'''