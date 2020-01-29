# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:38:24 2020

@author: Jan Kondracki
"""

import pymongo

def csvToDict(file_name):
	file = open(file_name, "r")
	lines = file.readlines()
	
	header = lines[0]
	splittedHead = header.split(',')
	counter = 0
	dictList = []
	
	for line in lines:
		if counter == 0:
			counter = counter + 1
			continue
		else:
			splittedLine = line.split(',')
			singleDict = {"_id": str(splittedLine[0])}
			for i in range(1, len(splittedHead)-1):
				if splittedLine[i] == 'nil':
					continue
				singleDict[str(splittedHead[i])] = splittedLine[i]
			dictList.append(singleDict)
			counter = counter + 1
	return dictList

def csvToGeoDict(file_name):
	file = open(file_name, "r")
	lines = file.readlines()
	
	header = lines[0]
	splittedHead = header.split(',')
	
	headCounter = 0
	for val in splittedHead:
		valSplitted = val.split('/')
		if valSplitted[1] == 'geometria':
			geoIdx = headCounter
			geoType = valSplitted[2]
			break
		headCounter += 1

	counter = 0
	dictList = []
	for line in lines:
		if counter == 0:
			counter = counter + 1
			continue
		else:
			splittedLine = line.split(',')
			singleDict = {"_id": str(splittedLine[0]), "type": "Feature", "geometry": {"type": geoType, "coordinates": splittedLine[geoIdx]}, "properties":{}}
			for i in range(1, len(splittedHead)-1):
				if i == geoIdx:
					continue
				
				if splittedLine[i] == '':
					continue
				else:
					singleDict["properties"][splittedHead[i]] = splittedLine[i]
			dictList.append(singleDict)
			counter = counter + 1
	return dictList


	
		 
def insertMongo(csv_file, collectionName, dbName):
	listDict = csvToGeoDict(csv_file)
	mydb = myclient[dbName]
	collection = mydb[collectionName]
	
	for dictio in listDict:
		collection.insert_one(dictio)
		
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\ADJA_A.csv", "ADJA_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\ADMS_A.csv", "ADMS_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\ADMS_P.csv", "ADMS_P", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTGN_A.csv", "PTGN_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTKM_A.csv", "PTKM_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTLZ_A.csv", "PTLZ_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTNZ_A.csv", "PTNZ_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTPL_A.csv", "PTPL_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTRK_A.csv", "PTRK_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTSO_A.csv", "PTSO_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTTR_A.csv", "PTTR_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTUT_A.csv", "PTUT_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTWP_A.csv", "PTWP_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTWZ_A.csv", "PTWZ_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\PTZB_A.csv", "PTZB_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\TCON_A.csv", "TCON_A", "BDOTGeoNoNull")
insertMongo("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\TCRZ_A.csv", "TCRZ_A", "BDOTGeoNoNull")

