# -*- coding: utf-8 -*-
import redis
import csv
import numpy as np
import pprint
from functions import *

#Sciezka do katalogu z danymi
sciezka_do_katalogu = 'C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok2\\'

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
ourDbStringGeo = redis.Redis(connection_pool=pool)

slowniki = czytanie_slownika(sciezka_do_katalogu+'PL.PZGiK.994.0463\\XSD\\OT_BDOT10k_Slowniki.xsd')
sciezka_dostepu = sciezka_do_katalogu+'converted_csv\\'
records = wsadowe_wczytywanie(sciezka_dostepu, 'csv')

def centeroidnp(arr):
	length = len(arr[0])
	sum_x = 0
	for x in arr[0]:
		sum_x += float(x)
	sum_y = 0
	for y in arr[1]:
		sum_y += float(y)
	return sum_x/length, sum_y/length

noID = 0
for key in records:
	header = key
	head = header.split(',')
	i = 0
	zapamietaj = []
	for attribute in head:
		attr = attribute.split('/')
		attr_name = attr[len(attr) - 2]
		attr_name = attr_name.replace(' ', '')
		if attr_name == 'posList':
			zapamietaj.append(i)
		i += 1
	the_class = records[key]
	for row in the_class:
		place = len(row) - 1
		objectkey = str(row[place])
		while objectkey.startswith('PL.PZGIK.BDOT10k') == False:
			place -= 1
			if place == 1:
				noID += 1
				objectkey = row[4][0:4] + str(noID)
				break
			objectkey = str(row[place])
		objectval = str(row).strip('[]')
		objectval = objectval.replace("'", "")
		tab_objects = objectval.split(',')
		iter = 0
		for obj_val in tab_objects:
			for pos in zapamietaj:
				if obj_val != tab_objects[pos]:
					obj_val = obj_val.replace(" ", "")
				else:
					tab_of_coords = obj_val.split(" ")
					arr = []
					iksy = []
					igreki = []
					for i in range(0,len(tab_of_coords)):
						if tab_of_coords[i] == '':
							continue
						else:
							if i%2 == 1:
								iksy.append(tab_of_coords[i])
							else:
								igreki.append(tab_of_coords[i])
					arr.append(iksy)
					arr.append(igreki)			
					X, Y = centeroidnp(arr)
					ourDbStringGeo.geoadd('positions', X, Y, objectkey)
			wart = obj_val.replace(' ', '')
			if obj_val in slowniki:
				wart = slowniki[obj_val]
				tab_objects[iter] = wart
			if wart == '':
				wart = 'null'
			if iter == 0:
				newobjectval = wart
			else:
				newobjectval = newobjectval + ', ' + wart
			iter += 1
		ourDbStringGeo.delete(objectkey)
		ourDbStringGeo.set(objectkey, newobjectval)

ptkm1 = 'PL.PZGIK.BDOT10k.PTKMA.04.6311'
ptkm2 = 'PL.PZGIK.BDOT10k.PTKMA.04.6310'
val = ourDbStringGeo.get(ptkm1)
posGeo = ourDbStringGeo.geopos('positions', ptkm2)
hashGeo = ourDbStringGeo.geohash('positions', ptkm2)
dist = ourDbStringGeo.geodist('positions', ptkm1, ptkm2)
print(val)
print('Pozycja: ', posGeo, 'Geohash: ', hashGeo)
print('Odleglosc: ', dist)