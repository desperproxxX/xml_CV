import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog
import os

def xml_set_label(path_xml, path_map):
    # Прописываем параметры xml в хэдере
    # path_xml = '/Users/anatolijrozkov/Desktop/xml CV parser/mil.xml'
    # path_map = '/Users/anatolijrozkov/Desktop/xml CV parser/меппинг.csv'

    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace('Calculation', "http://www.sap.com/ndb/BiModelCalculation.ecore")
    tree = ET.parse(path_xml)
    root = tree.getroot()
    attributes = 0
    measures = 0
    with open(path_map, encoding='utf-8') as f_maps:
        dct_for_iter = dict()
        con = csv.DictReader(f_maps, delimiter=';')
        for row in con:
            dct_for_iter[row['info_object'].strip()] = row['desc']

    for key, value in dct_for_iter.items():
        for element in root.findall('.//attribute[@id="' + key + '"]'):
            default_description = element.find('descriptions')
            if default_description is not None:
                default_description.set('defaultDescription', value)
                attributes += 1
        for element in root.findall('.//measure[@id="' + key + '"]'):
            default_description = element.find('descriptions')
            if default_description is not None:
                default_description.set('defaultDescription', value)
                measures += 1

    tree.write(os.path.join(os.path.dirname(path_xml), os.path.splitext(os.path.basename(path_xml))[0]+"_modified.xml"), encoding='utf-8', xml_declaration=True)

    info_label.config(text=f'Аттрибутов заменено: {attributes}\nПоказателей заменено: {measures}')

def open_file_xml():
    file_xml_label.config(text='')
    global file_xml
    file_xml = filedialog.askopenfilename(title="Выберите файл 1")
    file_xml_label.config(text=file_xml)



def open_file_csv():
    file_csv_label.config(text='')
    global file_csv
    file_csv = filedialog.askopenfilename(title="Выберите файл 2")
    file_csv_label.config(text=file_csv)

def toggle():
    flag_check = True
    try:
        if file_xml and os.path.basename(file_xml).split('.')[1] != 'xml':
            info_label.config(text='Некорректный файл xml')
            flag_check = False
        if file_csv and os.path.basename(file_csv).split('.')[1] != 'csv':
            info_label.config(text='Некорректный файл csv')
            flag_check = False
        if flag_check and file_xml_button and file_csv:
            xml_set_label(file_xml, file_csv)
    except:
        info_label.config(text='Выберите файлы')

# Создание окна
window = tk.Tk()
window.title("SAP HANA CV label desc")
window.geometry("400x250")

# Создание кнопок для выбора файлов
file_xml_button = tk.Button(window, text="Выбрать xml", command=open_file_xml)
file_xml_button.pack(pady=10)

file_xml_label = tk.Label(window, text="Файл 1: ")
file_xml_label.pack()

file_csv_button = tk.Button(window, text="Выбрать меппинг csv", command=open_file_csv)
file_csv_button.pack(pady=10)

file_csv_label = tk.Label(window, text="Файл 2: ")
file_csv_label.pack()

set_label_button = tk.Button(window, text="Выполнить", command=toggle)
set_label_button.pack(pady=10)

# Создание поля с информацией
info_label = tk.Label(window, text="Информация")
info_label.pack(pady=10)

# Запуск главного цикла
window.mainloop()
