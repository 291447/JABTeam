# -*- coding: utf-8 -*-
import arcpy
from a_star import *
from create_graf import *
from alt_path import *
import time

start = '464430.25,572320.14'
end = '481488.72,574638.42'
'''
start = '464430.25,572320.14'
end = '482347.92,575393.13'
'''
search_start_time = time.time()
#arcpy.env.workspace = "C:\\3rok\\sem5\\PAG2\\pag\\projekt\\Torun_jezdnie"
arcpy.env.workspace = "C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\Torun_jezdnie"
in_features = "L4_1_BDOT10k__OT_SKJZ_L.shp"
cursor = arcpy.SearchCursor(in_features)
print("--- %s seconds ---" % (time.time() - search_start_time))

graf_start_time = time.time()
graf = create_graf(cursor)
print("--- %s seconds ---" % (time.time() - graf_start_time))

A_Star_start_time = time.time()
#0 - dlugosc
#1 - czas
param = 0
outcome = A_star(graf, graf.node[start], graf.node[end], param)
if outcome == 0:
	print ('Path not found')
else:
	path, i = outcome
	print("--- %s seconds ---" % (time.time() - A_Star_start_time))
	expression = ""
	for single in path:
		if single != path[len(path) - 1]:
			expression = expression + '"FID" = ' + single + " OR "
		else:
			expression = expression + '"FID" = ' + single
			
	where_clause = expression

	arcpy.env.overwriteOutput = True
	arcpy.Select_analysis("C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\Torun_jezdnie\\L4_1_BDOT10k__OT_SKJZ_L.shp", "C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\shortest_path.shp", where_clause)

	arcpy.CreateFeatureclass_management('C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\', 'nody.shp', 'POLYLINE')
	'''
	fc = 'C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\nody.shp'
	cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"])
	array_of_points = []
	for point in path:
		pt = point.split(',')
		pt_x = float(pt[0])
		pt_y = float(pt[1])
		array_of_points.append(arcpy.Point(pt_x, pt_y))
	arcpy_array = arcpy.Array(array_of_points)
	spatial_reference = arcpy.SpatialReference(2180)
	polyline = arcpy.Polyline(arcpy_array, spatial_reference)
	cursor.insertRow([polyline])
	'''
	alt_path, alt_i = alt_path(path, graf, param, graf.node[start], graf.node[end])

	expression = ""
	for single in alt_path:
		if single != alt_path[len(alt_path) - 1]:
			expression = expression + '"FID" = ' + single + " OR "
		else:
			expression = expression + '"FID" = ' + single
			
	where_clause = expression

	arcpy.env.overwriteOutput = True
	arcpy.Select_analysis("C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\Torun_jezdnie\\L4_1_BDOT10k__OT_SKJZ_L.shp", "C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\alt_path.shp", where_clause)

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