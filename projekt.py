import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import os
#import pip
#import openpyxl
#pip install openpyxl do wiersza polecen
def leontief(input_file):
    macierz = pd.read_excel(input_file, header=None)#wczytujemy macierz używając biblioteki pandas
    macierz = macierz.values
    wiersze, kolumny = macierz.shape
    macierz_jednostkowa = np.eye(wiersze, kolumny)
    leontief = macierz_jednostkowa - macierz  # wyświetlamy macierz Leontiefa
    if np.linalg.det(leontief) == 0:  # sprawdzamy czy jest odwracalna, czyli czy wyznacznik wynosi 0
        print("Macierz z wyznacznikiem rownym 0")
        return None
    elif wiersze != kolumny:  # sprawdzamy czy jest kwadratowa
        print("Macierz nie jest kwadratowa")
        return None
    else:
        return leontief

def odwr_leontief(input_file):
    macierz = pd.read_excel(input_file, header=None)#wczytujemy macierz używając biblioteki pandas
    macierz=macierz.values
    wiersze, kolumny = macierz.shape
    macierz_jednostkowa = np.eye(wiersze, kolumny)
    leontief = (macierz_jednostkowa - macierz)  # wyświetlamy macierz Leontiefa
    if np.linalg.det(leontief) == 0:  # sprawdzamy czy jest odwracalna, czyli czy wyznacznik wynosi 0
        print("Macierz nieodwracalna")
        return None
    elif wiersze != kolumny:  # sprawdzamy czy jest kwadratowa
        print("Macierz nie jest kwadratowa")
        return None
    else:
        macierz_odwrotna = np.linalg.inv(leontief)  # dzięki bibliotece numpy możemy jedną komendą odwrócić macierz
        return macierz_odwrotna

def oblicz_calkowity(input_file, y_file, output_file):
    try:
        macierz_odwrotna = odwr_leontief(input_file)
        macierz_y = pd.read_excel(y_file, header=None)
        macierz_y=macierz_y.values
        w, k = macierz_y.shape
        if k != 1:
            return "Nieprawidłowa liczba kolumn."
        if macierz_odwrotna.shape[1] != macierz_y.shape[0]:
            return "Nie można pomnożyć, ponieważ liczba kolumn nie jest równa liczbie wierszy."
        produkcja_calkowita = np.matmul(macierz_odwrotna, macierz_y)
        print("Produkcja całkowita:")
        print(produkcja_calkowita)
        produkcja_calkowita_df = pd.DataFrame(produkcja_calkowita)
        if os.path.isfile(output_file):
            return "Plik wyjściowy już istnieje."
        else:
            produkcja_calkowita_df.to_excel(output_file, index=False, header=False)
            return "Pomyślnie zapisano wynik."

    except FileNotFoundError:
        return "Nie istnieje plik z podanej ścieżki."
    except Exception as e:
        return "Wystąpił błąd."

def oblicz_finalny(input_file, x_file, output_file):
    try:
        macierz_leontiefa = leontief(input_file)
        macierz_x = pd.read_excel(x_file, header=None)
        macierz_x=macierz_x.values
        w, k = macierz_x.shape
        if k != 1:
            return "Nieprawidłowa liczba kolumn."
        if macierz_leontiefa.shape[1] != macierz_x.shape[0]:
            return "Nie można pomnożyć, ponieważ liczba kolumn nie jest równa liczbie wierszy."
        produkcja_finalna = np.matmul(macierz_leontiefa, macierz_x)
        print("Produkcja finalna:")
        print(produkcja_finalna)
        produkcja_finalna_df = pd.DataFrame(produkcja_finalna)
        if os.path.isfile(output_file):
            return "Plik wyjściowy już istnieje."
        else:
            produkcja_finalna_df.to_excel(output_file, index=False, header=False)
            return "Pomyślnie zapisano wynik."

    except FileNotFoundError:
        return "Nie istnieje plik z podanej ścieżki."
    except Exception as e:
        return "Wystąpił błąd."

class Przeplywy_Miedzygaleziowe:

    def __init__(self, master):
        self.master = master
        master.title("Tablice input-output")

        self.input_label = tk.Label(master, text="Macierz nakladow:",font=("Times New Roman", 13,"bold" ),width=15, height=2)
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        self.input_button = tk.Button(master, text="Przegladaj",bg="white", command=self.przegladaj_naklady,width=10,height=2)
        self.input_button.grid(row=0, column=1,columnspan=2)

        self.y_label = tk.Button(master, text="Plik wejsciowy y:",font=("Times New Roman", 13, "bold"),width=15, height=2)
        self.y_label.grid(row=1, column=0, padx=10, pady=10)
        self.y_button = tk.Button(master, text="Przegladaj",bg="white" ,command=self.przegladaj_y,width=10,height=2)
        self.y_button.grid(row=1, column=1,columnspan=2)

        self.x_label = tk.Label(master, text="Plik wejsciowy x:",font=("Times New Roman", 13,"bold" ),width=15, height=2)
        self.x_label.grid(row=2, column=0, padx=10, pady=10)
        self.x_button = tk.Button(master, text="Przegladaj",bg="white", command=self.przegladaj_x,width=10,height=2)
        self.x_button.grid(row=2, column=1,columnspan=2)

        self.calculate_calkowity_button = tk.Button(master, text="Oblicz calkowity(x)",font=("Times New Roman", 14, "bold"), command=self.oblicz_calkowity,width=20, height=2)
        self.calculate_calkowity_button.grid(row=4, column=0, padx=10, pady=10)
        self.calculate_finalny_button = tk.Button(master, text="Oblicz finalny(y)",font=("Times New Roman", 14, "bold"), command=self.oblicz_finalny,width=20, height=2)
        self.calculate_finalny_button.grid(row=4, column=1, padx=10, pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.quit_button = tk.Button(master, text="Wyjdz",font=("Times New Roman", 14, "bold"), command=master.quit,width=20, height=2)
        self.quit_button.grid(row=5, column=0,columnspan=2,  padx=10, pady=10)

    def quit(self):
        self.master.quit()

    def przegladaj_naklady(self):
        self.input_file = filedialog.askopenfilename(title="Wybierz macierz nakladow",
                                                   filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        try:
            input_matrix = pd.read_excel(self.input_file,header=None)
            w,k=input_matrix.shape
            if w != k:
                self.status_label.config(text="Wczytana macierz nie jest kwadratowa.")
                self.input_file = None
            else:
                self.status_label.config(text="Poprawne wczytanie pliku")
        except:
            self.status_label.config(text="Błąd wczytywania pliku.")
            self.input_file = None

    def przegladaj_y(self):
        self.y_file = filedialog.askopenfilename(title="Wybierz y", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        try:
            y_matrix = pd.read_excel(self.y_file)
            if y_matrix.shape[1] != 1:
                self.status_label.config(text="Wczytana macierz musi mieć tylko jedną kolumnę.")
                self.y_file = None
            else:
                self.status_label.config(text="Poprawne wczytanie pliku")
        except:
            self.status_label.config(text="Błąd wczytywania pliku.")
            self.y_file = None

    def przegladaj_x(self):
        self.x_file = filedialog.askopenfilename(title="Wybierz x", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        try:
            x_matrix = pd.read_excel(self.x_file)
            if x_matrix.shape[1] != 1:
                self.status_label.config(text="Wczytana macierz musi mieć tylko jedną kolumnę.")
                self.x_file = None
            else:
                self.status_label.config(text="Poprawne wczytanie pliku")
        except:
            self.status_label.config(text="Błąd wczytywania pliku.")
            self.x_file = None

    def oblicz_calkowity(self):
        if hasattr(self, 'input_file') and hasattr(self, 'y_file'):
            self.output_file = filedialog.asksaveasfilename(title="Zapisz plik jako", defaultextension=".xlsx",filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            status = oblicz_calkowity(self.input_file, self.y_file,self.output_file)
            self.status_label.config(text=status)
        else:
            self.status_label.config(text="Nie udało się wykonać operacji: brak jednego z plików.")

    def oblicz_finalny(self):
        if hasattr(self, 'input_file') and hasattr(self, 'x_file'):
            self.output_file = filedialog.asksaveasfilename(title="Zapisz plik jako", defaultextension=".xlsx",filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
            status = oblicz_finalny(self.input_file, self.x_file, self.output_file)
            self.status_label.config(text=status)
        else:
            self.status_label.config(text="Nie udało się wykonać operacji: brak jednego z plików.")

root = tk.Tk()
root.configure(background='purple')
przeplywy_gui = Przeplywy_Miedzygaleziowe(root)
root.mainloop()

