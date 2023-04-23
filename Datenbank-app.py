import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import re
from tkinter.simpledialog import askstring
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

try:
    connection = pymysql.connect(host="127.0.0.1", user="root", passwd="", database="epi_db_final")
    cursor = connection.cursor()
except:
    print("Keine Verbindung möglich")




regex = "^[0-3]?[0-9][/.][0-3]?[0-9][/.](?:[0-9]{2})?[0-9]{2}$"
regex_ZID = "^[0-9]{1,4}$"
regex_Göße = "^[1-2]{1}[4-9]{1}[0-9]{1}$"
regex_gewicht = "^[1-9]{1}[0-9]{2}"
regex_id_Suche = "^[0-9]{1,4}$"
regex_name_Suche = "^[a-zA-Z]{3,15}$"


def main():
    root = tk.Tk()
    root.geometry("500x500")
    # root.resizable(False,False)

    name_main = tk.StringVar()
    name2_main = tk.StringVar()
    Datum_Aufnahme = tk.StringVar()
    Zentren_ID = tk.StringVar()
    Größe_VA = tk.StringVar()
    Gewicht = tk.StringVar()
    gesch_var = tk.StringVar()

    def zur_ück():
        root.destroy()
        command_window()

    def Speichern():

        Name_Main_Var_speich = name_main.get()
        Name2_Main_Speich = name2_main.get()
        Datum_Aufnahme_Speichern = Datum_Aufnahme.get()
        Zentren_ID_Speichern = Zentren_ID.get()
        Größe_VA_Speicher = Größe_VA.get()
        Gewicht_Speicher = Gewicht.get()
        SX_geschle_var = gesch_var.get()

        insert1 = (
            "INSERT INTO idat" "(Name, Nachname, Aufnahme_Datum, Zentrums_ID, Gewicht, Größe, SEX)" "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        insert1_data = (
        Name_Main_Var_speich, Name2_Main_Speich, Datum_Aufnahme_Speichern, Zentren_ID_Speichern, Gewicht_Speicher,
        Größe_VA_Speicher, SX_geschle_var)
        cursor.execute(insert1, insert1_data)
        connection.commit()
        cursor.execute("SELECT ID from idat ORDER BY ID DESC LIMIT 1")

        id = cursor.fetchall()

        clean_id = re.sub('[\W ]', '', str(id))
        root.destroy()

        def exposition():
            expo_root_window = tk.Tk()
            expo_root_window.geometry("600x1000")

            raucher_radio_var = tk.StringVar()
            was_rauchen_radio_var = tk.StringVar()
            var_entry_alter_rauchen = tk.StringVar()
            var_falls_ehmal_wann_kein_rauch = tk.StringVar()
            var_Zigaretten_wie_viel = tk.StringVar()
            var_radio_derzeit_alk = tk.StringVar()
            var_wie_viel_alk = tk.StringVar()
            var_radio_gesund_bedenken = tk.StringVar()

            def expo():
                Raucher = raucher_radio_var.get()
                was_Raucher = was_rauchen_radio_var.get()
                alter_b_rauch = var_entry_alter_rauchen.get()
                falls_ehm = var_falls_ehmal_wann_kein_rauch.get()
                zig_wie_viel = var_Zigaretten_wie_viel.get()
                der_zeit_alk = var_radio_derzeit_alk.get()
                viel_alk = var_wie_viel_alk.get()
                gesund_bedenken = var_radio_gesund_bedenken.get()

                insert2 = (
                    "INSERT INTO mdat" "(ID, schon_Geraucht, was_Rauchen, alter_rauchen_bego, ex_raucher_seit, durchschnitt_zig, alkohol_wie_oft, wie_viel_alk, bedenken_gesundheit)" "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                insert2_data = (
                clean_id, Raucher, was_Raucher, alter_b_rauch, falls_ehm, zig_wie_viel, der_zeit_alk, viel_alk,
                gesund_bedenken)
                cursor.execute(insert2, insert2_data)
                connection.commit()

                expo_root_window.destroy()
                command_window()

            def zurück():
                expo_root_window.destroy()
                main()

            def disable_rauche():
                raucher_was_radio.config(state="disabled")
                raucher_was_radio2.config(state="disabled")
                entry_falls_Sie_Zigaretten.config(state="disabled")
                entry_Falls_ehmalig.config(state="disabled")
                entry_Pfeife_oder_Zigarette_Alter.config(state="disabled")
                entry_falls_Sie_Zigaretten.config(state="disabled")

            def normal_rauchen():
                raucher_was_radio.config(state="normal")
                raucher_was_radio2.config(state="normal")
                entry_falls_Sie_Zigaretten.config(state="normal")
                entry_Falls_ehmalig.config(state="normal")
                entry_Pfeife_oder_Zigarette_Alter.config(state="normal")
                entry_falls_Sie_Zigaretten.config(state="normal")

            def disable_alk():
                entry_wie_viel_alkohol.config(state="disabled")

            def normal_alk():
                entry_wie_viel_alkohol.config(state="normal")

            expo_root_window.grid_columnconfigure(1, weight=3)

            titel_label = ttk.Label(expo_root_window, text="Expositionserhebung bei Aufnahme", font=("Helvetica 20"))
            titel_label.grid(column=0, row=0, columnspan=3)

            label_raucher_frage = tk.Label(expo_root_window,
                                           text="Haben Sie schon einmal geraucht oder rauchen Sie zur Zeit?",
                                           relief="solid", justify="left")
            label_raucher_frage.grid(column=0, row=2, sticky=tk.NW, padx=10, pady=40)

            raucher_radio_box = ttk.Radiobutton(expo_root_window, text="nie", value=0, variable=raucher_radio_var,
                                                command=disable_rauche)
            raucher_radio_box.grid(column=1, row=2)
            raucher_radio_box2 = ttk.Radiobutton(expo_root_window, text="ehemalig", value=1, variable=raucher_radio_var,
                                                 command=normal_rauchen)
            raucher_radio_box2.grid(column=2, row=2, ipadx=10)

            label_was_rsuchen = tk.Label(expo_root_window, text="Wenn ja: was rauchen Sie zur Zeit?", relief="solid",
                                         justify="left")
            label_was_rsuchen.grid(column=0, row=3, sticky=tk.NW, pady=40, padx=10)

            raucher_was_radio = ttk.Radiobutton(expo_root_window, text="Preife", value=1,
                                                variable=was_rauchen_radio_var)
            raucher_was_radio.grid(column=1, row=3, pady=40)

            raucher_was_radio2 = ttk.Radiobutton(expo_root_window, text="Zigarette", value=0,
                                                 variable=was_rauchen_radio_var)
            raucher_was_radio2.grid(column=2, row=3, padx=10, pady=40)

            label_Fall_Pfeife_oder_Zigarette = tk.Label(expo_root_window,
                                                        text="Falls Pfeife oder Zigaretten:\nIn welchem Alter wurde mit dem Rauchen begonnen",
                                                        relief="solid", justify="left")
            label_Fall_Pfeife_oder_Zigarette.grid(column=0, row=4, sticky=tk.NW, padx=10, pady=40)

            entry_Pfeife_oder_Zigarette_Alter = tk.Entry(expo_root_window, textvariable=var_entry_alter_rauchen)
            entry_Pfeife_oder_Zigarette_Alter.grid(column=1, row=4, columnspan=2, sticky=tk.EW, padx=20)

            label_Falls_ehemalig = tk.Label(expo_root_window,
                                            text="Falls ehemalig:\nSeit wann sind Sie kein Raucher mehr?",
                                            relief="solid", justify="left")
            label_Falls_ehemalig.grid(column=0, row=5, pady=40, sticky=tk.NW, padx=10)

            entry_Falls_ehmalig = tk.Entry(expo_root_window, textvariable=var_falls_ehmal_wann_kein_rauch)
            entry_Falls_ehmalig.grid(column=1, row=5, columnspan=2, sticky=tk.EW, padx=20)

            label_Falls_Sie_Zigaretten_geraucht_haben = tk.Label(expo_root_window,
                                                                 text="Falls Sie Zigaretten geraucht haben:\nWie viele Zigaretten wurden durchschnittlich pro Taggeraucht",
                                                                 relief="solid", justify="left")
            label_Falls_Sie_Zigaretten_geraucht_haben.grid(column=0, row=6, pady=40, sticky=tk.W, padx=10, )

            entry_falls_Sie_Zigaretten = tk.Entry(expo_root_window, textvariable=var_Zigaretten_wie_viel)
            entry_falls_Sie_Zigaretten.grid(column=1, row=6, columnspan=2, sticky=tk.EW, padx=20)

            label_Wie_Alkohol = tk.Label(expo_root_window, text="Wie oft trinken Sie derzeit Alkohol?", relief="solid",
                                         justify="left")
            label_Wie_Alkohol.grid(column=0, row=7, pady=40, sticky=tk.NW, padx=10)

            radio_wie_oft_alkohlo_nie = ttk.Radiobutton(expo_root_window, text="Nie", variable=var_radio_derzeit_alk,
                                                        value=0, command=disable_alk)
            radio_wie_oft_alkohlo_nie.grid(column=1, row=7, pady=40)
            radio_wie_oft_alkohlo_geleg = ttk.Radiobutton(expo_root_window, text="Gelegentlich",
                                                          variable=var_radio_derzeit_alk, value=1, command=normal_alk)
            radio_wie_oft_alkohlo_geleg.grid(column=2, row=7, pady=40)
            radio_wie_oft_alkohlo_taglich = ttk.Radiobutton(expo_root_window, text="Täglich",
                                                            variable=var_radio_derzeit_alk, value=3, command=normal_alk)
            radio_wie_oft_alkohlo_taglich.grid(column=3, row=7, pady=40)

            label_Falls_Alkohol = tk.Label(expo_root_window,
                                           text="Falls Sie derzeit Alkohol trinken:\n Wie viel Gramm trinken Sie ungefähr pro Tag?\n(1 Bier (500ml) = 20g oder 1/4l Wein = 20g)",
                                           relief="solid", justify="left")
            label_Falls_Alkohol.grid(column=0, row=9, pady=40, sticky=tk.NW, padx=10, )

            entry_wie_viel_alkohol = tk.Entry(expo_root_window, textvariable=var_wie_viel_alk)
            entry_wie_viel_alkohol.grid(column=1, row=9, pady=40, sticky=tk.EW, padx=10, columnspan=2)

            label_Gesundheit_bedenken = tk.Label(expo_root_window, text="Haben Sie gesundheitliche Bedenken?",
                                                 relief="solid", justify="left")
            label_Gesundheit_bedenken.grid(column=0, row=10, pady=40, sticky=tk.NW, padx=10)

            radio_gesundheit_bedenken_keine = ttk.Radiobutton(expo_root_window, text="Nein",
                                                              variable=var_radio_gesund_bedenken, value=0)
            radio_gesundheit_bedenken_keine.grid(column=1, row=10, pady=40)
            radio_gesundheit_bedenken_unter = ttk.Radiobutton(expo_root_window, text="unter Umständen",
                                                              variable=var_radio_gesund_bedenken, value=1)
            radio_gesundheit_bedenken_unter.grid(column=2, row=10, pady=40)
            radio_gesundheit_bedenken_ja = ttk.Radiobutton(expo_root_window, text="Ja",
                                                           variable=var_radio_gesund_bedenken, value=3)
            radio_gesundheit_bedenken_ja.grid(column=3, row=10, pady=40)

            label_leer = tk.Label(expo_root_window, text="")
            label_leer.grid(column=0, row=1, pady=20, sticky=tk.NW)

            expo_button = tk.Button(expo_root_window, text="Speichern", command=expo)
            expo_button.grid(column=3, row=11, sticky=tk.NW)

            expo_button = tk.Button(expo_root_window, text="Zurück", command=zurück)
            expo_button.grid(column=2, row=11, sticky=tk.NW)

            expo_root_window.mainloop()

        exposition()

    def validate(input):
        if (re.search(regex, input)):
            print(True)
            Speicher_Butoon.config(state="active")
            return True
        else:
            print(False)
            Speicher_Butoon.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format TT.MM.JJJJ ihr angabe wahr {Datum_Aufnahme.get()}")
            return False

    def validate_ZID(input):
        if (re.search(regex_ZID, input)):
            print(True)
            Speicher_Butoon.config(state="active")
            return True
        else:
            print(False)
            Speicher_Butoon.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format NNNN ihr angabe wahr {Zentren_ID.get()}")
            return False

    def validate_Größe(input):
        if (re.search(regex_Göße, input)):
            print(True)
            Speicher_Butoon.config(state="active")
            return True
        else:
            print(False)
            Speicher_Butoon.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format NNN keine führende nulll ihr angabe wahr {Größe_VA.get()}")
            return False

    def validate_Gewicht(input):
        if (re.search(regex_gewicht, input)):
            print(True)
            Speicher_Butoon.config(state="active")
            return True
        else:
            print(False)
            Speicher_Butoon.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format NNN keine führende nulll ihr angabe wahr {Größe_VA.get()}")
            return False

    def validate_Name(input):
        if (re.search(regex_name_Suche, input)):
            print(True)
            Speicher_Butoon.config(state="active")
            return True
        else:
            print(False)
            Speicher_Butoon.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte geben Sie Ihren Vornamen ein {name_main.get()}")
            return False

    def validate_Name2(input):
        if (re.search(regex_name_Suche, input)):
            print(True)
            Speicher_Butoon.config(state="active")
            return True
        else:
            print(False)
            Speicher_Butoon.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte geben Sie Ihren Nachnamen ein {name2_main.get()}")
            return False

    my_val = root.register(validate)
    my_val_ZID = root.register(validate_ZID)
    my_val_Größe = root.register(validate_Größe)
    my_val_Gewicht = root.register(validate_Gewicht)
    my_val_Name = root.register(validate_Name)
    my_val_Name2 = root.register(validate_Name2)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    Name_Main_Var = tk.Label(root, text="Vorname")
    Name_Main_Var.grid(column=0, row=0, sticky=tk.W, ipady=20, ipadx=20)
    Name_Main_Var_eingabe = tk.Entry(root, textvariable=name_main, validate="focusout",
                                     validatecommand=(my_val_Name, "%P"))
    Name_Main_Var_eingabe.grid(column=1, row=0, sticky=tk.EW, padx=5)

    Name2_Main_Var = tk.Label(root, text="Nachrname")
    Name2_Main_Var.grid(column=0, row=1, sticky=tk.W, ipady=20, ipadx=20)
    Name2_Main_Var_eingabe = tk.Entry(root, textvariable=name2_main, validate="focusout",
                                      validatecommand=(my_val_Name2, "%P"))
    Name2_Main_Var_eingabe.grid(column=1, row=1, sticky=tk.EW, padx=5)
    Aufnahme_datum = tk.Label(root, text="Aufnahmedatum: ")
    Aufnahme_datum.grid(column=0, row=2, sticky=tk.W, ipadx=20, ipady=20)
    Aufnahme_datum_eingabe = tk.Entry(root, textvariable=Datum_Aufnahme, validate="focusout",
                                      validatecommand=(my_val, "%P"))
    Aufnahme_datum_eingabe.grid(column=1, row=2, sticky=tk.EW, padx=5)

    Studien_Zentrum = tk.Label(root, text="Zentrums_ID: ")
    Studien_Zentrum.grid(column=0, row=3, sticky=tk.W, ipadx=20, ipady=20)
    Studien_Zentrum_eingabe = tk.Entry(root, textvariable=Zentren_ID, validate="focusout",
                                       validatecommand=(my_val_ZID, "%P"))
    Studien_Zentrum_eingabe.grid(column=1, row=3, sticky=tk.EW, padx=5)

    Größe = tk.Label(root, text=" Größe: ")
    Größe.grid(column=0, row=4, sticky=tk.W, ipadx=20, ipady=20)
    größe_eingabe = tk.Entry(root, textvariable=Größe_VA, validate="focusout", validatecommand=(my_val_Größe, "%P"))
    größe_eingabe.grid(column=1, row=4, sticky=tk.EW, padx=5)

    gewicht = tk.Label(root, text="Gewicht: ")
    gewicht.grid(column=0, row=5, sticky=tk.W, ipadx=20, ipady=20)
    Gewicht_eingabe = tk.Entry(root, textvariable=Gewicht, validate="focusout", validatecommand=(my_val_Gewicht, "%P"))
    Gewicht_eingabe.grid(column=1, row=5, sticky=tk.EW, padx=5)

    sex = tk.Radiobutton(root, text="Mänlich", value="M", variable=gesch_var)
    sex2 = tk.Radiobutton(root, text="Weiblich", value="W", variable=gesch_var)

    sex.grid(column=1, row=6, sticky=tk.NW)
    sex2.grid(column=1, row=6, sticky=tk.NS, ipadx=10)

    Speicher_Butoon = tk.Button(root, text="Speichern", command=Speichern)
    Speicher_Butoon.grid(column=1, row=7, pady=50)

    Speicher_Butoon2 = tk.Button(root, text="Zurück", command=zur_ück)
    Speicher_Butoon2.grid(column=0, row=7, pady=50)

    root.mainloop()


def command_window():
    def calli():
        Erstes_Fenster.destroy()
        main()

    def Suche():
        Erstes_Fenster.destroy()
        Suche_fkt()

    def follow_com():
        Erstes_Fenster.destroy()
        fol_up()

    def Plot_com():
        Erstes_Fenster.destroy()
        ploti()

    Erstes_Fenster = tk.Tk()
    Erstes_Fenster.geometry("300x300")
    Buttoon1 = tk.Button(Erstes_Fenster, text="Befragung", command=calli).pack(fill="x")
    Buttoon2 = tk.Button(Erstes_Fenster, text="Suchen", command=Suche).pack(fill="x")
    Buttoon3 = tk.Button(Erstes_Fenster, text="follow Up", command=follow_com).pack(fill="x")
    Buttoon4 = tk.Button(Erstes_Fenster, text="Plot", command=Plot_com).pack(fill="x")
    Erstes_Fenster.mainloop()


def Suche_fkt():
    def Zuruck():
        Such_fenster.destroy()
        command_window()

    Such_fenster = tk.Tk()
    Such_fenster.geometry("1400x500")

    def suche_db():
        name_Suche_DB = name_Suche.get()
        name2_Suche_DB = name2_Suche.get()
        global data_DB
        uw = "SELECT * FROM idat WHERE Vorname LIKE %s OR Nachname LIKE %s", [name_Suche_DB, name2_Suche_DB]

        # insert_suche = ("SELECT * fROM  stammdaten" "WHERE Vorname AND Nachname" "(%s, %s)",(name_Suche_DB,name2_Suche_DB))
        # insert_suche_data = (insert_suche,(name_Suche_DB,name2_Suche_DB))
        cursor.execute("SELECT * FROM idat WHERE Name = %s AND Nachname = %s", [name_Suche_DB, name2_Suche_DB])

        fetch = cursor.fetchall()

        for data in fetch:
            my_tree.insert("", "end", values=data)

            # my_tree.insert('', 'end', values=row[0:6])

            # data_DB = cursor.fetchall()

        data_DB = pd.DataFrame(cursor.fetchall(),
                               columns=["Nachname", "Vorname", "ID", "Aufnahmedatum", "Zentrums_ID", "Größe",
                                        "Gewicht"])
        print(data_DB)

    def suche_x_y():
        global x
        global y
        global hue_
        x = askstring('X', "X Achse")
        y = askstring('hue', 'Y Achse')
        hue_ = askstring('hue', 'Trennung')

        def b_plot():
            sns.set_theme(style="ticks", palette="pastel")
            # tips = sns.load_dataset(data_DB)
            sns.boxplot(x=f"{x}", y=f"{y}",
                        hue=f"{hue_}",
                        data=data_DB)
            sns.despine(offset=10, trim=True)

        b_plot()

    def validate_ID(input):
        if (re.search(regex_id_Suche, input)):
            print(True)
            Such_Button_Suche.config(state="active")
            return True
        else:
            print(False)
            Such_Button_Suche.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format TT.MM.JJJJ ihr angabe wahr {id_Suche.get()}")
            return False

    def validate_name(input):
        if (re.search(regex_name_Suche, input)):
            print(True)
            Such_Button_Suche.config(state="active")
            return True
        else:
            print(False)
            Such_Button_Suche.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format NNNN ihr angabe wahr {name_Suche.get()}")
            return False

    def validate_name2(input):
        if (re.search(regex_name_Suche, input)):
            print(True)
            Such_Button_Suche.config(state="active")
            return True
        else:
            print(False)
            Such_Button_Suche.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format NNN keine führende nulll ihr angabe wahr {name2_Suche.get()}")
            return False

    id_Suche = tk.StringVar()
    name_Suche = tk.StringVar()
    name2_Suche = tk.StringVar()
    Such_fenster.columnconfigure(1, weight=1)
    # Such_fenster.rowconfigure(5,weight=5)

    my_val_ID = Such_fenster.register(validate_ID)
    my_val_name = Such_fenster.register(validate_name)
    my_val_name2 = Such_fenster.register(validate_name2)

    Id_V = tk.Label(Such_fenster, text=" ID:")
    Id_V.grid(row=0, column=0, pady=20)
    ID_entry = tk.Entry(Such_fenster, textvariable=id_Suche, validate="focusout", validatecommand=(my_val_ID, "%P"))
    ID_entry.grid(row=0, column=1, sticky=tk.EW, padx=20, )

    name = tk.Label(Such_fenster, text="Name:")
    name.grid(row=1, column=0, pady=20)
    Name_entry = tk.Entry(Such_fenster, textvariable=name_Suche, validate="focusout",
                          validatecommand=(my_val_name, "%P"))
    Name_entry.grid(row=1, column=1, sticky=tk.EW, padx=20)

    name2 = tk.Label(Such_fenster, text="Nachname:")
    name2.grid(row=2, column=0, pady=20)
    Name2_entry = tk.Entry(Such_fenster, textvariable=name2_Suche, validate="focusout",
                           validatecommand=(my_val_name2, "%P"))
    Name2_entry.grid(row=2, column=1, sticky=tk.EW, padx=20)

    tree_scroll = ttk.Scrollbar(Such_fenster)
    tree_scroll.grid(column=2, rowspan=4, columnspan=4, sticky=tk.NW)

    my_tree = ttk.Treeview(Such_fenster, yscrollcommand=tree_scroll.set, selectmode="extended", show="headings")
    my_tree.grid(column=0, columnspan=3, rowspan=2, row=4, sticky=tk.EW, padx=20)
    my_tree["columns"] = ("1", "2", "3", "4", "5", "6", "7")
    my_tree.heading('1', text='ID')
    my_tree.heading('2', text='Vorname')
    my_tree.heading('3', text='Nachname')
    my_tree.heading('4', text='Aufnahmedatum')
    my_tree.heading('5', text='Zentrums_ID')
    my_tree.heading('6', text='Gewicht')
    my_tree.heading('7', text='Größe')

    Such_Button_Suche = tk.Button(Such_fenster, text="Suchen", command=suche_db)
    Such_Button_Suche.grid(column=1, row=3, sticky=tk.EW, padx=20, pady=10)

    Plot_button = tk.Button(Such_fenster, text="Plot", command=suche_x_y)
    Plot_button.grid(column=2, row=3, sticky=tk.EW, padx=20, pady=10)

    Zurück_Button = tk.Button(Such_fenster, text="Zurück", command=Zuruck)
    Zurück_Button.grid(column=0, row=3, pady=10)

    Such_fenster.mainloop()


def fol_up():
    follow = tk.Tk()
    follow.geometry("300x380")
    style = ttk.Style()
    style.theme_use("vista")
    follow.columnconfigure(1, weight=3)

    id_label = tk.StringVar()
    wenn_ja_datum = tk.StringVar()
    verstorben = tk.StringVar()
    infarkt = tk.StringVar()

    def follow_speichern():
        id_follow_id_speich = id_label.get()
        wenn_follow_Speich = wenn_ja_datum.get()
        infarkt_speicher = infarkt.get()
        verstorben_speichern = verstorben.get()

        insert1 = ("INSERT INTO fol_ow" "(ID, infarkt, Verstorben, Todes_Datum)"
                   "VALUES (%s, %s, %s, %s)")
        insert1_data = (id_follow_id_speich, infarkt_speicher, verstorben_speichern, wenn_follow_Speich)
        cursor.execute(insert1, insert1_data)
        connection.commit()
        follow.destroy()
        fol_up()

    def follow_zuruck():
        follow.destroy()
        command_window()

    def validate(input):
        if (re.search(regex, input)):
            print(True)
            speicherbutton_follow_up.config(state="active")
            return True
        else:
            print(False)
            speicherbutton_follow_up.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format TT.MM.JJJJ ")
            return False

    def validate_ZID(input):
        if (re.search(regex_ZID, input)):
            print(True)
            speicherbutton_follow_up.config(state="active")
            return True
        else:
            print(False)
            speicherbutton_follow_up.config(state="disabled")
            tk.messagebox.showinfo(title="Falsches format",
                                   message=f"Bitte wenden sie das format NNNN ")
            return False

    val_id_label = follow.register(validate_ZID)
    val_wenn_ja_datum = follow.register(validate)

    id_label_follow = tk.Label(follow, text="ID")
    id_label_follow.grid(column=0, row=2, sticky=tk.NW, pady=30, padx=20)
    id_label_entry = tk.Entry(follow, textvariable=id_label, validate="focusout", validatecommand=(val_id_label, "%P"))
    id_label_entry.grid(column=1, row=2, sticky=tk.EW, padx=10, columnspan=2)

    infar_var = tk.StringVar()
    infar_label_follow = tk.Label(follow, text="Infarct")
    infar_label_follow.grid(column=0, row=3, sticky=tk.NW, pady=30, padx=20)
    infar = ttk.Radiobutton(follow, text="JA", value="ja", variable=infarkt)
    infar2 = ttk.Radiobutton(follow, text="Nein", value="nein", variable=infarkt)
    infar.grid(column=1, row=3)
    infar2.grid(column=2, row=3, padx=30)

    versorbe_var = tk.StringVar()
    verstor_label_follow = tk.Label(follow, text="Verstorben")
    verstor_label_follow.grid(column=0, row=4, sticky=tk.NW, pady=30, padx=20)
    ver = ttk.Radiobutton(follow, text="Ja", value="JA", variable=verstorben)
    ver2 = ttk.Radiobutton(follow, text="nein", value="Nein", variable=verstorben)
    ver.grid(column=1, row=4)
    ver2.grid(column=2, row=4, padx=30)

    wennja_label_follow = tk.Label(follow, text="wenn ja wann")
    wennja_label_follow.grid(column=0, row=5, sticky=tk.NW, pady=30, padx=20)
    wennja_entry = tk.Entry(follow, textvariable=wenn_ja_datum, validate="focusout",
                            validatecommand=(val_wenn_ja_datum, "%P"))
    wennja_entry.grid(column=1, row=5, sticky=tk.EW, padx=10, columnspan=2)

    button_zuru_follow = tk.Button(follow, text="zurück", command=follow_zuruck)
    button_zuru_follow.grid(column=0, row=6, sticky=tk.EW, rowspan=2, pady=15, padx=15, )

    speicherbutton_follow_up = tk.Button(follow, text="Speichern", command=follow_speichern)
    speicherbutton_follow_up.grid(column=1, row=6, sticky=tk.EW, columnspan=2, pady=15, padx=15)

    follow.mainloop()


def ploti():
    q2 = "show TABLES from epi_db_final"
    plot = tk.Tk()
    plot.geometry("500x500")
    sele_ction2 = tk.StringVar()
    cursor.execute(q2)
    Tabellenname = cursor.fetchall()

    clean_Tabellenname = []
    tabellename_in_liste = list(Tabellenname)
    count = 0
    for idx, object in enumerate(tabellename_in_liste):
        clean_schleife_Tabname = re.sub('[\W \d]', '', str(object))
        clean_Tabellenname.append(clean_schleife_Tabname)

    for data in clean_Tabellenname:
        auswahl_Tab = ttk.Radiobutton(plot, text=f"{clean_Tabellenname[count]}", value=f"{clean_Tabellenname[count]}",
                                      variable=sele_ction2).grid(column=2, row=count, sticky=tk.NW)
        count += 1

    def Spalten():
        plot.destroy()

        spalten = tk.Tk()

        Tabelen_name = sele_ction2.get()
        selection_Spalten_name = tk.StringVar()
        selection_Spalten_name2 = tk.StringVar()

        cursor.execute("select column_name from information_schema.columns where table_name= %s", [Tabelen_name])
        sequence = cursor.fetchall()
        clean_spalten_name = []
        Spalten_namen_in_Liste = list(sequence)
        count = 0
        for idx, object in enumerate(Spalten_namen_in_Liste):
            clean_spalten_name_schleife = re.sub('[\W \d]', '', str(object))
            clean_spalten_name.append(clean_spalten_name_schleife)

        for data in clean_spalten_name:
            auswahl_Tab = ttk.Radiobutton(spalten, text=f"{clean_spalten_name[count]}", value=clean_spalten_name[count],
                                          variable=selection_Spalten_name).grid(column=2, row=count, sticky=tk.NW)
            auswahl_Tab = ttk.Radiobutton(spalten, text=f"{clean_spalten_name[count]}", value=clean_spalten_name[count],
                                          variable=selection_Spalten_name2).grid(column=3, row=count, sticky=tk.NW)
            count += 1

        def Box_P():
            engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@127.0.0.1:3306/epi_db_final")
            col_list = []
            X = selection_Spalten_name.get()
            Y = selection_Spalten_name2.get()
            col_list.append(X)
            col_list.append(Y)

            # query = "select f"{X}",f"{Y}" From table_name= F"{Tabelen_name}""
            # cursor.execute("select %s,%s From table_name = %s", [X, Y, Tabelen_name])
            pandas_datafram = pd.read_sql_table(table_name=Tabelen_name, columns=col_list, con=engine)
            # pandas_datafram = pd.read_sql("select %s,%s From table_name = %s", [X, Y, Tabelen_name],connection)

            sns.boxplot(x=f"{X}", y=f"{Y}", data=pandas_datafram)
            plt.show()

        def Bae_P():
            engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@127.0.0.1:3306/epi_db_final")
            col_list = []
            X = selection_Spalten_name.get()
            Y = selection_Spalten_name2.get()
            col_list.append(X)
            col_list.append(Y)

            # query = "select f"{X}",f"{Y}" From table_name= F"{Tabelen_name}""
            # cursor.execute("select %s,%s From table_name = %s", [X, Y, Tabelen_name])
            pandas_datafram = pd.read_sql_table(table_name=Tabelen_name, columns=col_list, con=engine)
            # pandas_datafram = pd.read_sql("select %s,%s From table_name = %s", [X, Y, Tabelen_name],connection)

            sns.countplot(x=f"{X}", hue=f"{Y}", data=pandas_datafram)
            plt.show()

        def plot_zu():
            engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@127.0.0.1:3306/epi_db_final")
            col_list = []
            X = selection_Spalten_name.get()
            Y = selection_Spalten_name2.get()
            col_list.append(X)
            col_list.append(Y)

            # query = "select f"{X}",f"{Y}" From table_name= F"{Tabelen_name}""
            # cursor.execute("select %s,%s From table_name = %s", [X, Y, Tabelen_name])
            pandas_datafram = pd.read_sql_table(table_name=Tabelen_name, columns=col_list, con=engine)
            # pandas_datafram = pd.read_sql("select %s,%s From table_name = %s", [X, Y, Tabelen_name],connection)

            sns.scatterplot(x=f"{X}", y=f"{Y}", data=pandas_datafram)
            plt.show()

        def zuruck():
            spalten.destroy()
            ploti()

        n1 = tk.Button(spalten, text="Box-Plot", command=Box_P).grid(column=0, row=8)
        n1 = tk.Button(spalten, text="Scater-Plot", command=plot_zu).grid(column=2, row=8)
        n1 = tk.Button(spalten, text="Barchart", command=Bae_P).grid(column=3, row=8)
        n2 = tk.Button(spalten, text="Zurück", command=zuruck).grid(column=1, row=8)

        spalten.mainloop()

    def Box():
        plot.destroy()
        Box_window = tk.Tk()

        Box_window.mainloop()

    def Zuruck_com():
        plot.destroy()
        command_window()

    Buttoon1 = tk.Button(plot, text="Auswahl", command=Spalten).grid(column=0, row=3)
    Buttoon2 = tk.Button(plot, text="Zurück", command=Zuruck_com).grid(column=0, row=4)

    plot.mainloop()





if __name__ == '__main__':
    command_window()


