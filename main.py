import xml.etree.ElementTree as ET
import csv
from tkinter import filedialog
import os
import customtkinter


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

    info_label.configure(text=f'Аттрибутов заменено: {attributes}\nПоказателей заменено: {measures}')

def open_file_xml():
    global file_xml
    file_xml = filedialog.askopenfilename(title="Выберите файл xml")
    file_xml_label.configure(text=file_xml)



def open_file_csv():
    global file_csv
    file_csv = filedialog.askopenfilename(title="Выберите файл csv")
    file_csv_label.configure(text=file_csv)

def toggle():
    flag_check = True
    try:
        if file_xml and os.path.basename(file_xml).split('.')[1] != 'xml':
            info_label.configure(text='Некорректный файл xml')
            flag_check = False
        if file_csv and os.path.basename(file_csv).split('.')[1] != 'csv':
            info_label.configure(text='Некорректный файл csv')
            flag_check = False
        if flag_check and file_xml and file_csv:
            xml_set_label(file_xml, file_csv)
    except KeyError:
        info_label.configure(text='В csv файле нет 1-й строки: desc; info_object ')
    except NameError:
        info_label.configure(text='Не выбран файл')

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
window = customtkinter.CTk()  # create window
window.title('XML change lables')
window.geometry("400x250")
fr = customtkinter.CTkFrame(window, width=400, height=200)
fr.pack(padx=10, pady=10)

# Configure the rows and columns of the grid
fr.columnconfigure(0, minsize=200)
for i in range(7):
    fr.rowconfigure(i, minsize=30)

file_xml_button = customtkinter.CTkButton(fr, text="Выбрать xml", command=open_file_xml, width=300)
file_xml_button.grid(row=0, column=0, sticky="ew", padx=20)

file_xml_label = customtkinter.CTkLabel(fr, text="Файл xml: ")
file_xml_label.grid(row=1, column=0, sticky="w", padx=20)

file_csv_button = customtkinter.CTkButton(fr, text="Выбрать меппинг csv", command=open_file_csv)
file_csv_button.grid(row=2, column=0, sticky="ew", padx=20)

file_csv_label = customtkinter.CTkLabel(fr, text="Файл csv: ")
file_csv_label.grid(row=3, column=0, sticky="w", padx=20)

set_label_button = customtkinter.CTkButton(fr, text="Выполнить", command=toggle)
set_label_button.grid(row=4, column=0, sticky="ew", padx=20)

info_label = customtkinter.CTkLabel(fr, text="Информация")
info_label.grid(row=5, column=0, sticky="w", padx=20, pady=20)

window.mainloop()
# window = customtkinter.CTk()  # create window
# window.geometry("400x300")
# fr = customtkinter.CTkFrame(window, width=400, height=200)
# fr.pack(padx=20, pady=20)
#
# file_xml_button = customtkinter.CTkButton(fr, text="Выбрать xml", command=open_file_xml)
# file_xml_button.grid(row=0, column=0, padx=100, pady=10)
#
# file_xml_label = customtkinter.CTkLabel(fr, text="Файл 1: ")
# file_xml_label.grid(row=1, column=0, padx=100, pady=10)
#
# file_csv_button = customtkinter.CTkButton(fr, text="Выбрать меппинг csv", command=open_file_csv)
# file_csv_button.grid(row=3, column=0, padx=100, pady=10)
#
# file_csv_label = customtkinter.CTkLabel(fr, text="Файл 2: ")
# file_csv_label.grid(row=4, column=0, padx=100, pady=10)
#
# set_label_button = customtkinter.CTkButton(fr, text="Выполнить", command=toggle)
# set_label_button.grid(row=5, column=0, padx=100, pady=10)
#
# info_label = customtkinter.CTkLabel(fr, text="Информация")
# info_label.grid(row=6, column=0, padx=100, pady=10)
#
# window.mainloop()
