# -*- coding: utf-8 -*-
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
our_db = redis.Redis(connection_pool=pool)

#PL.PZGIK.BDOT10k.PTGNA.04.632

import csv

def wczytywanie_csv(plik):
	allrows = []
	with open(str(plik), 'r') as csvFile:
		reader = csv.reader(csvFile)
		head = 0
		for row in reader:
			if head == 0:
				head = 1
			else:
				allrows.append(row)
	print (len(allrows))			
	csvFile.close()
	return allrows

def wsadowe_wczytywanie(sciezka_dostepu, ext):
	import glob
	import os
	
	print('Tworzenie wsadowej konwersji plikow')
	if ext == 'csv':
		pliki_sfery = glob.glob(sciezka_dostepu+'*.'+ext)
		print(pliki_sfery)
		sciezka_sfery = os.path.dirname(pliki_sfery[0])
		
		tabOfRecords = []
		k = 0
		for i in range(0,len(pliki_sfery)):
			k = i + 1
			print('Wczytywanie pliku csv nr: ', k)
			tabOfRecords.append(wczytywanie_csv(pliki_sfery[i]))
			
	else:
		print('Bledne rozszerzenie')
		tabOfRecords = 0
		
	return tabOfRecords

sciezka_dostepu = 'C:\\Users\\annas\\Documents\\3_rok\\PAG\\blok2\\csvs\\'
records = wsadowe_wczytywanie(sciezka_dostepu, 'csv')

for the_class in records:
	for row in the_class:
		objectkey = row[2]
		#print(objectkey)
		objectval = str(row).strip('[]')
		#print(objectval)
		our_db.set(objectkey, objectval)
print(our_db.dbsize())

val = our_db.get('PL.PZGIK.BDOT10k.PTLZA.04.6324')
print(val)
