# -*- coding: utf-8 -*-
import redis
import numpy as np
from functions import *

#Sciezka do katalogu z danymi
sciezka_do_katalogu = 'C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok2\\'

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
ourDbString = redis.Redis(connection_pool=pool)

slowniki = czytanie_slownika(sciezka_do_katalogu+'PL.PZGiK.994.0463\\XSD\\OT_BDOT10k_Slowniki.xsd')
sciezka_dostepu = sciezka_do_katalogu+'converted_csv\\'
records = wsadowe_wczytywanie(sciezka_dostepu, 'csv')

noID = 0
for key in records:
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
			wart = obj_val
			wart = wart.replace(' ', '')
			if wart == '':
				wart = 'null'
			if wart in slowniki:
				wart = slowniki[wart]
				tab_objects[iter] = wart
			if iter == 0:
				newobjectval = wart
			else:
				newobjectval = newobjectval + ', ' + wart
			iter += 1
		ourDbString.delete(objectkey)
		ourDbString.set(objectkey, newobjectval)
		
val = ourDbString.get('PL.PZGIK.BDOT10k.PTKMA.04.6310')
print(val)