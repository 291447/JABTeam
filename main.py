# -*- coding: utf-8 -*-
import arcpy
from a_star import *
from create_graf import *
from alt_path import *
import time
import os

sciezka = "C:\\3rok\\sem5\\PAG2\\pag\\projekt\\"
newpath = r"C:\\3rok\\sem5\\PAG2\\pag\\projekt\\wyniki" 
if not os.path.exists(newpath):
    os.makedirs(newpath)
'''
start = '471263.18,572530.82'
end = '471482.73,572529.94'

start = '464430.25,572320.14'
end = '482347.92,575393.13'
'''


search_start_time = time.time()
arcpy.env.workspace = sciezka + "Torun_jezdnie"
in_features = "powiat_torun.shp"
cursor = arcpy.da.SearchCursor(in_features, ["OID@", "SHAPE@" ,"SHAPE@LENGTH", 'klasaDrogi'])
print('Search time: ', "--- %s seconds ---" % (time.time() - search_start_time))

graf_start_time = time.time()
graf = create_graf(cursor)
print('Create graph time: ', "--- %s seconds ---" % (time.time() - graf_start_time))

input_features = 'wybrane_punkty.shp'
input_points =  arcpy.da.SearchCursor(input_features, ["SHAPE@X", "SHAPE@Y"])
x = []
y = []
for row in input_points:
	xx = row[0]
	x.append(xx)
	yy = row[1]
	y.append(yy)

start = str(x[0])+','+str(y[0])
end = str(x[1])+','+str(y[1])
print(start, end)

A_Star_start_time = time.time()
#0 - dlugosc
#1 - czas
param = 1
outcome = A_star(graf, start, end, param)
if outcome == 0:
	print ('Path not found')
else:
	path, i, total = outcome
	expression = ""
	for single in path:
		if single != path[len(path) - 1]:
			expression = expression + '"FID" = ' + single + " OR "
		else:
			expression = expression + '"FID" = ' + single
			
	where_clause = expression

	arcpy.env.overwriteOutput = True
	arcpy.Select_analysis(sciezka + "Torun_jezdnie\\powiat_torun.shp", sciezka + "Wyniki\\shortest_path.shp", where_clause)

	print('Create path time: ', "--- %s seconds ---" % (time.time() - A_Star_start_time))
	if param == 1:
		total = total/60
		unit = 'min'
	else:
		unit = 'm'
	print('Total for path: ', total, unit)
	'''
	arcpy.CreateFeatureclass_management(sciezka + 'Wyniki\\', 'nody.shp', 'POLYLINE')
	fc = sciezka + 'Wyniki\\nody.shp'
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
	alt_path_start_time = time.time()
	outcome = alt_path(path, graf, param, start, end)
	if outcome == 0:
		print('Alternative path not found')
	else:
		alt_path, alt_i, total = outcome
		expression = ""
		for single in alt_path:
			if single != alt_path[len(alt_path) - 1]:
				expression = expression + '"FID" = ' + single + " OR "
			else:
				expression = expression + '"FID" = ' + single
				
		where_clause = expression

		arcpy.env.overwriteOutput = True
		arcpy.Select_analysis(sciezka + "Torun_jezdnie\\powiat_torun.shp", sciezka + "Wyniki\\alt_path.shp", where_clause)
		print('Create alternative path time: ', "--- %s seconds ---" % (time.time() - alt_path_start_time))
		if param == 1:
			total = total/60
			unit = 'min'
		else:
			unit = 'm'
		print('Total for alternative path: ', total, unit)

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