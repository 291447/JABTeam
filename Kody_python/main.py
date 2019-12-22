# -*- coding: utf-8 -*-
import arcpy
from a_star import *
from create_graf import *
from alt_path import *
import time
import os

sciezka = "C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\" #sciezka, w ktorej jest folder 'Dane' z potrzebnymi danymi shapefile

#stworzenie folderu, w ktorym maja byc stworzone wyniki
newpath = r"C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok1\\projekt\\Wyniki"
if not os.path.exists(newpath):
    os.makedirs(newpath)
	
search_start_time = time.time()

#wybranie danych
in_points = sciezka + "Dane\\wybrane_punkty.shp"
in_features = sciezka + "Dane\\powiat_torun.shp"

#wydobycie wspolrzednych wybranych punktow
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

#stworzenie kursora po danych shapefile potrzebnych do stworzenia grafu
cursor = arcpy.da.SearchCursor(in_features, ["OID@", "SHAPE@" ,"SHAPE@LENGTH", 'klasaDrogi'])

print('Search time: ', "%s seconds" % (time.time() - search_start_time))

#tworzenie grafu
graf_start_time = time.time()
graf = create_graf(cursor)

print('Create graph time: ', "%s seconds" % (time.time() - graf_start_time))

#param = 0 - szukanie drogi po dlugosci
#param = 1 - szukanie drogi po czasie
param = 0

A_Star_start_time = time.time()

#uruchomienie algorytmu A*
outcome = A_star(graf, start, end, param)

print('Create path time: ', "%s seconds" % (time.time() - A_Star_start_time))

#sprawdzenie, czy zostala wygenerowana droga
if outcome == 0:
	print ('Path not found')
else:
	#przypisanie wartosci
	path, i, total = outcome
	
	#tworzenie wyrazenia po klauzuli WHERE sluzacego do wyboru odcinkow drogi, nalezacych do znalezionej sciezki
	expression = ""
	for single in path:
		if single != path[len(path) - 1]:
			expression = expression + '"FID" = ' + single + " OR "
		else:
			expression = expression + '"FID" = ' + single

	arcpy.env.overwriteOutput = True
	
	#stworzenie najkrotszej sciezki jako pliku shapefile
	arcpy.Select_analysis(sciezka + "Dane\\powiat_torun.shp", sciezka + "Wyniki\\shortest_path.shp", expression)

	if param == 1:
		total = total/60
		unit = 'min'
	else:
		unit = 'm'
	print('Total for path: ', total, unit)
	
	alt_path_start_time = time.time()
	
	#wyszukiwanie alternatywnej sciezki
	outcome = alt_path(path, graf, param, start, end)
	
	#sprawdzenie, czy zostala wygenerowana
	if outcome == 0:
		print('Alternative path not found')
	else:
		alt_path, alt_i, total = outcome
		
		#tworzenie wyrazenia po klauzuli WHERE sluzacego do wyboru odcinkow drogi, nalezacych do znalezionej sciezki
		expression = ""
		for single in alt_path:
			if single != alt_path[len(alt_path) - 1]:
				expression = expression + '"FID" = ' + single + " OR "
			else:
				expression = expression + '"FID" = ' + single

		arcpy.env.overwriteOutput = True
		
		#stworzenie alternatywnej sciezki jako pliku shapefile
		arcpy.Select_analysis(sciezka + "Dane\\powiat_torun.shp", sciezka + "Wyniki\\alt_path.shp", expression)
		
		print('Create alternative path time: ', "%s seconds" % (time.time() - alt_path_start_time))
		
		if param == 1:
			total = total/60
			unit = 'min'
		else:
			unit = 'm'
		print('Total for alternative path: ', total, unit)