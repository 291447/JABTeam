# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:06:26 2020

@author: kondr
"""
import os


def correctCSV(file_namer, file_namew):
    file = open(file_namer, "r")
    lines = file.readlines()
    header = lines[0]
    hd2 = header.replace(":","")
    hd2 = hd2.replace("/","")
    file.close()
    file = open(file_namew, "w")
    file.write(hd2)
    for i in range(1,len(lines)-1):
        file.write(lines[i])
    file.close()
#correctCSV("D:\\zadania\\sem5\\pag\\blok2\\csv_converted\\ADJA_A.csv", 'D:\\zadania\\sem5\\pag\\blok2\\neo4j\\ADJA_Anowy.csv')

def csvToCypher(file_name, cypherTxtFile, feature_name):
    file = open(file_name, "r")
    name = os.path.split(file_name)[1]
    lines = file.readlines()
    header = lines[0].rstrip().split(",")
    #hd2 = header.replace(":",";")
    file.close()

    file = open(cypherTxtFile, "w")
    
    file.write("LOAD CSV WITH HEADERS FROM " + "'file:///C:/" + name +"'"+ " AS csvLine\n")
    
    cline = []
    for head in header:
        cline.append(head+": "+"csvLine."+head)
    
    cline = ",".join(cline)
    file.write("CREATE ("+"b"+":"+feature_name+ "{"+cline+"})")
    file.close()
    
csvToCypher('D:\\zadania\\sem5\\pag\\blok2\\neo4j\\ADMS_Anowy.csv', 'D:\\zadania\\sem5\\pag\\blok2\\neo4j\\cypher.txt', "ADMS_A" )
    
    


    