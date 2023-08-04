import tkinter as tk
from tkinter import filedialog
import subprocess


def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def run_script_in_background():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    try:
        subprocess.Popen(["python", "clean_xml.py", input_file, output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_label.config(text="Le script a été lancé en arrière-plan.")
    except Exception as e:
        status_label.config(text="Une erreur s'est produite : " + str(e))

root = tk.Tk()
root.title("Application avec GUI")

title_label = tk.Label(root, text="Application avec GUI")
title_label.pack(pady=10)

input_file_button = tk.Button(root, text="Choisir le fichier d'entrée", command=select_input_file)
input_file_button.pack()

input_file_entry = tk.Entry(root, width=50)
input_file_entry.pack()

output_file_button = tk.Button(root, text="Choisir l'emplacement et le nom du fichier de sortie", command=select_output_file)
output_file_button.pack()

output_file_entry = tk.Entry(root, width=50)
output_file_entry.pack()

run_button = tk.Button(root, text="Lancer le script en arrière-plan", command=run_script_in_background)
run_button.pack()

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()
