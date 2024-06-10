import xml.etree.ElementTree as ET
import csv
from tkinter import filedialog
import os
import customtkinter



def xml_set_label(path_xml, path_map):
    tree = ET.parse(path_xml)
    root = tree.getroot()
    for param, uri in ET.iterparse(path_xml, events=['start-ns']):
        ET.register_namespace(uri[0], uri[1])
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
    # Чекаем ветку

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
window.geometry("380x280")
fr = customtkinter.CTkFrame(window, width=380, height=250, corner_radius=10)
fr.pack(side="left", padx=10, pady=10)
fr.grid_propagate(False)
# fr.grid(row=0, column=0, padx=10, pady=10)


# fr_xml_settings = customtkinter.CTkFrame(window, width=370, height=200, corner_radius=10)
# fr_xml_settings.pack(side="right", padx=10, pady=10, fill="both", expand=True)
# fr_xml_settings.grid_propagate(False)


# Configure the rows and columns of the grid
fr.columnconfigure(0, minsize=200)
for i in range(7):
    fr.rowconfigure(i, minsize=30)

# xsi = customtkinter.CTkEntry(fr_xml_settings, width=350)
# xsi.insert('0', 'http://www.w3.org/2001/XMLSchema-instance')
# xsi.grid(row=0, column=0, sticky="ew", padx=20)

file_xml_button = customtkinter.CTkButton(fr, text="Выбрать xml", command=open_file_xml, width=300)
file_xml_button.grid(row=0, column=0, sticky="ew", padx=20)

file_xml_label = customtkinter.CTkLabel(fr, text="Файл xml: ",  wraplength=350, font=('Tahoma', 11))
file_xml_label.grid(row=1, column=0, sticky="w", padx=20)

file_csv_button = customtkinter.CTkButton(fr, text="Выбрать меппинг csv", command=open_file_csv)
file_csv_button.grid(row=2, column=0, sticky="ew", padx=20)

file_csv_label = customtkinter.CTkLabel(fr, text="Файл csv: ",  wraplength=350, font=('Tahoma', 11))
file_csv_label.grid(row=3, column=0, sticky="w", padx=20)

set_label_button = customtkinter.CTkButton(fr, text="Выполнить", command=toggle)
set_label_button.grid(row=4, column=0, sticky="ew", padx=20)

info_label = customtkinter.CTkLabel(fr, text="Информация",  wraplength=350, font=('Tahoma', 12))
info_label.grid(row=5, column=0, sticky="w", padx=20, pady=20)

window.mainloop()
