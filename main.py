# -*- coding: utf-8 -*-
import arcpy
from a_star import *
from create_graf import *
from alt_path import *
import time

search_start_time = time.time()
arcpy.env.workspace = "C:\\3rok\\sem5\\PAG2\\pag\\projekt\\Torun_jezdnie"
#arcpy.env.workspace = "C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\Torun_jezdnie"
in_features = "L4_1_BDOT10k__OT_SKJZ_L.shp"
cursor = arcpy.SearchCursor(in_features)
print("--- %s seconds ---" % (time.time() - search_start_time))

graf_start_time = time.time()
graf = create_graf(cursor)
print("--- %s seconds ---" % (time.time() - graf_start_time))
print(len(graf.node))

A_Star_start_time = time.time()
param = 0
path, i, path_edge = A_star(graf, graf.node['464430.25,572320.14'], graf.node['481488.72,574638.42'], param)
print("--- %s seconds ---" % (time.time() - A_Star_start_time))

#print(path, "liczba iter: ", i, "dlugosc sciezki: ", len(path), path_edge, len(path_edge))

expression = ""
for single in path_edge:
	if single != path_edge[len(path_edge) - 1]:
		expression = expression + '"FID" = ' + single + " OR "
	else:
		expression = expression + '"FID" = ' + single
		
where_clause = expression

#print(where_clause)
arcpy.env.overwriteOutput = True
arcpy.Select_analysis("C:\\3rok\\sem5\\PAG2\\pag\\projekt\\Torun_jezdnie\\L4_1_BDOT10k__OT_SKJZ_L.shp", "C:\\3rok\\sem5\\PAG2\\pag\\projekt\\shortest_path.shp", where_clause)

arcpy.CreateFeatureclass_management('C:\\3rok\\sem5\\PAG2\\pag\\projekt', 'droga.shp', 'POLYLINE')

fc = 'C:\\3rok\\sem5\\PAG2\\pag\\projekt\\droga.shp'
cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"])
array_of_points = []
for point in path:
	pt = point.split(',')
	pt_x = float(pt[0])
	pt_y = float(pt[1])
	array_of_points.append(arcpy.Point(pt_x, pt_y))
	#array = arcpy.Array([arcpy.Point(-77.4349451, 37.5408265),
	#					 arcpy.Point(-78.6384349, 35.7780943)])
arcpy_array = arcpy.Array(array_of_points)
spatial_reference = arcpy.SpatialReference(2180)
polyline = arcpy.Polyline(arcpy_array, spatial_reference)
cursor.insertRow([polyline])

alt_path, alt_i, alt_path_edge = alt_path(path_edge, graf, param)

expression = ""
for single in alt_path_edge:
	if single != alt_path_edge[len(alt_path_edge) - 1]:
		expression = expression + '"FID" = ' + single + " OR "
	else:
		expression = expression + '"FID" = ' + single
		
where_clause = expression

#print(where_clause)
arcpy.env.overwriteOutput = True
arcpy.Select_analysis("C:\\3rok\\sem5\\PAG2\\pag\\projekt\\Torun_jezdnie\\L4_1_BDOT10k__OT_SKJZ_L.shp", "C:\\3rok\\sem5\\PAG2\\pag\\projekt\\alt_path.shp", where_clause)

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