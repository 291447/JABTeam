import csv

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
	
	#print('Tworzenie wsadowej konwersji plikow')
	if ext == 'csv':
		pliki_sfery = glob.glob(sciezka_dostepu+'*.'+ext)
		sciezka_sfery = os.path.dirname(pliki_sfery[0])
		
		tabOfRecords = {}
		#k = 0
		for i in range(0,len(pliki_sfery)):
			#k = i + 1
			#print('Wczytywanie pliku csv nr: ', k)
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