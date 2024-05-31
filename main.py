import xml.etree.ElementTree as ET
import csv

# Прописываем параметры xml в хэдере
path_xml = '/Users/anatolijrozkov/Desktop/xml CV parser/mil.xml'
path_map = '/Users/anatolijrozkov/Desktop/xml CV parser/меппинг.csv'

ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace('Calculation', "http://www.sap.com/ndb/BiModelCalculation.ecore")
tree = ET.parse(path_xml)
root = tree.getroot()
with open(path_map, encoding='utf-8') as f_maps:
    dct_for_iter = {}
    con = csv.DictReader(f_maps, delimiter=';')
    for row in con:
        dct_for_iter[row['info_object'].strip()] = row['desc']

for key, value in dct_for_iter.items():
    for element in root.findall('.//attribute[@id="'+key+'"]'):
        default_description = element.find('descriptions')
        if default_description is not None:
            default_description.set('defaultDescription', value)

for key, value in dct_for_iter.items():
    for element in root.findall('.//measure[@id="'+key+'"]'):
        default_description = element.find('descriptions')
        if default_description is not None:
            default_description.set('defaultDescription', value)

tree.write('/Users/anatolijrozkov/Desktop/xml CV parser/modified.xml', encoding='utf-8', xml_declaration=True)


