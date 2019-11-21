#import xml.etree.ElementTree as ET
#import csv
'''
tree = ET.parse("C:\3rok\sem5\PAG2\blok2\kujawsko_pomorskie_m_Torun_0463\PL.PZGiK.994.0463\BDOT10K\PL.PZGiK.994.0463__OT_ADJA_A.xml")
root = tree.getroot()

# open a file for writing

Resident_data = open('C:/3rok/sem5/PAG2/blok2/tmp/new_csv_data.csv', 'w')
'''
# create the csv writer object
'''
import xml.etree.ElementTree as ET
import xmltodict
import json

tree = ET.parse('C:\\3rok\\sem5\\PAG2\\blok2\\kujawsko_pomorskie_m_Torun_0463\\PL.PZGiK.994.0463\\BDOT10K\\PL.PZGiK.994.0463__OT_ADJA_A.xml')
xml_data = tree.getroot()

xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')


data_dict = dict(xmltodict.parse(xmlstr))

print(data_dict)

with open('C:\\3rok\\sem5\\PAG2\\blok2\\newJsonData.json', 'w+') as json_file:
    json.dump(data_dict, json_file, indent=4, sort_keys=True)
'''
'''
NS = 'urn:gugik:specyfikacje:gmlas:bazaDanychObiektowTopograficznych10k:1.0'
from xml.etree.ElementTree import parse, Element

doc = parse('C:\\3rok\\sem5\\PAG2\\blok2\\kujawsko_pomorskie_m_Torun_0463\\PL.PZGiK.994.0463\\BDOT10K\\PL.PZGiK.994.0463__OT_ADJA_A.xml')

root = doc.getroot()

for ot in root.iter('{%s}ot' % NS):
	print(ot)
'''
'''	
for child in root:
	rt = child
	for child1 in rt:
		rt1 = child1
		for child2 in rt1:
			print(child2.tag, child2.attrib)
'''
import xml.etree.ElementTree as ET
tree = ET.parse('C:\\3rok\\sem5\\PAG2\\blok2\\kujawsko_pomorskie_m_Torun_0463\\PL.PZGiK.994.0463\\BDOT10K\\PL.PZGiK.994.0463__OT_ADJA_A.xml')
root = tree.getroot()

# find the first 'item' object
for elem in root:
    print(elem.find('item').get('name'))

# find all "item" objects and print their "name" attribute
for elem in root:
    for subelem in elem.findall('item'):
    
        # if we don't need to know the name of the attribute(s), get the dict
        print(subelem.attrib)      
    
        # if we know the name of the attribute, access it directly
        print(subelem.get('name'))