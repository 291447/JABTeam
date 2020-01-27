# -*- coding: utf-8 -*-
import pickle
import redis
import csv
import numpy as np
import pprint

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
ourDbString = redis.Redis(connection_pool=pool)

def centeroidnp(arr):
	length = len(arr[0])
	sum_x = 0
	for x in arr[0]:
		sum_x += float(x)
	sum_y = 0
	for y in arr[1]:
		sum_y += float(y)
	X = sum_x/length
	Y = sum_y/length
	#inProj = Proj(init='epsg:2180')
	#outProj = Proj(init='epsg:4326')
	#X_t, Y_t = transform(inProj, outProj, X, Y)
	return X, Y

def czytanie_slownika(plik):
	TC = "SlownikiTerenyChronione"
	PT = "SlownikiPokrycieTerenu"
	AD = "SlownikiPodzialTerytorialny"
	SO = "SlownikiOgolne"
	enVal = "enumeration value"
	attr = "gml:description"
	found = 0
	slowniki = {}
	SlownikiFile = open(plik, 'r')
	fread = SlownikiFile.readlines()
	for line in fread:
		if (("!--" in line) and (found == 2)):
			found = 1
			continue
		if ((TC in line) or (PT in line) or (AD in line) or (SO in line)):
			found = 2
			continue
		if found == 1:
			if "!--" in line:
				found = 0
				continue
			elif enVal in line:
				enVal_val = line
				enVal_val = enVal_val.replace('<enumeration value="','')
				enVal_val = enVal_val.replace('">','')
				enVal_val = enVal_val.replace('\t','')
				enVal_val = enVal_val.replace('\n','')
			elif attr in line:
				attr_val = line
				attr_val = attr_val.replace('<gml:description>','')
				attr_val = attr_val.replace('</gml:description>','')
				attr_val = attr_val.replace('\t','')
				attr_val = attr_val.replace('\n','')
				slowniki[enVal_val] = attr_val
				
	return slowniki

slowniki = czytanie_slownika('C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok2\\PL.PZGiK.994.0463\\XSD\\OT_BDOT10k_Slowniki.xsd')

def wczytywanie_csv(plik):
	allrows = []
	with open(str(plik), 'r') as csvFile:
		reader = csv.reader(csvFile)
		head = 0
		for row in reader:
			if head == 0:
				header = str(row)
				header = header.replace('[','')
				header = header.replace(']','')
				header = header.replace("'",'')
				head = 1
			else:
				allrows.append(row)			
	csvFile.close()
	return header, allrows

def wsadowe_wczytywanie(sciezka_dostepu, ext):
	import glob
	import os
	
	print('Tworzenie wsadowej konwersji plikow')
	if ext == 'csv':
		pliki_sfery = glob.glob(sciezka_dostepu+'*.'+ext)
		sciezka_sfery = os.path.dirname(pliki_sfery[0])
		
		tabOfRecords = {}
		k = 0
		for i in range(0,len(pliki_sfery)):
			k = i + 1
			print('Wczytywanie pliku csv nr: ', k)
			header, rows = wczytywanie_csv(pliki_sfery[i])
			for r in rows:
				if header in tabOfRecords:
					tabOfRecords[header].append(r)
				else:
					tabOfRecords[header] = [r]
			
	else:
		print('Bledne rozszerzenie')
		tabOfRecords = 0
		
	return tabOfRecords
	
sciezka_dostepu = 'C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok2\\converted_csv\\'
records = wsadowe_wczytywanie(sciezka_dostepu, 'csv')
sdf = 0
for key in records:
	#the_class = records[1]
	header = key
	attr_list = []
	head = header.split(',')
	i = 0
	zapamietaj = []
	for attribute in head:
		attr = attribute.split('/')
		attr_name = attr[len(attr) - 2]
		attr_name = attr_name.replace(' ', '')
		attr_list.append(attr_name)
		if attr_name == 'posList':
			zapamietaj.append(i)
		i += 1
	the_class = records[key]
	for row in the_class:
		sdf += 1
		objectkey = str(row[len(row) - 1])
		objectval = str(row).strip('[]')
		objectval = objectval.replace("'", "")
		tab_objects = objectval.split(',')
		#if sdf > 100 and sdf < 120:
		#	print('lens', len(attr_list), len(tab_objects))
		iter = 0
		for obj_val in tab_objects:
			wart = obj_val
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
			if obj_val in slowniki:
				wart = slowniki[obj_val]
				tab_objects[iter] = wart
			wart = wart.replace(' ', '')
			if iter == 0:
				newobjectval = wart
			else:
				newobjectval = newobjectval + ', ' + wart
			iter += 1
		ourDbString.set(objectkey, newobjectval)
		
val = ourDbString.get('PL.PZGIK.BDOT10k.ADJAA.04.631')
print(val)