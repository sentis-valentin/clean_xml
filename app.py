import tkinter as tk
from tkinter import filedialog
import subprocess
import requests
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
import time
import logging

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
        # Lancer le script en arrière-plan en utilisant le module subprocess
        subprocess.Popen(["python", "clean_xml.py", input_file, output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_label.config(text="Le script a été lancé en arrière-plan.")
    except Exception as e:
        status_label.config(text="Une erreur s'est produite : " + str(e))

# Créer une fenêtre Tkinter
root = tk.Tk()
root.title("Application avec GUI")

# Ajouter des éléments à la fenêtre
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

# Démarrer la boucle Tkinter
root.mainloop()

# Configurer la journalisation vers un fichier log
logging.basicConfig(filename='logs.txt', level=logging.DEBUG)

def fetch_data_from_api(url, max_retries=5, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifiez si la réponse contient des erreurs HTTP
            return response.content
        except requests.exceptions.RequestException as e:
            logging.error(f"Une erreur s'est produite lors de la récupération des données : {e}")
            logging.info(f"Tentative de réessai ({retries+1}/{max_retries}) dans {retry_delay} secondes...")
            retries += 1
            time.sleep(retry_delay)
    raise Exception("Impossible de récupérer les données après plusieurs tentatives.")

def process_data(df_urls):
    # Liste pour stocker les données
    data = []

    # Parcourir les URLs d'API
    for index, api_url in enumerate(df_urls['api_url'], start=1):
        try:
            # Récupérez les données depuis l'API avec gestion d'erreur et réessai
            xml_data = fetch_data_from_api(api_url)

            # Analysez le contenu XML de la réponse avec BeautifulSoup
            soup = BeautifulSoup(xml_data, "xml")

            # Récupérez les balises dc:identifier et dc:relation
            identifiers = soup.find_all("dc:identifier")
            relations = soup.find_all("dc:relation")
            source = soup.find_all("dc:source")

            # Parcourez les balises dc:identifier et dc:relation
            for identifier, relation, source in zip(identifiers, relations, source):
                identifier_text = identifier.get_text() if identifier else ""
                relation_text = relation.get_text() if relation else ""
                source_text = source.get_text() if source else ""
                data.append([identifier_text, relation_text, source_text])
        except Exception as e:
            logging.exception(f"Une erreur inattendue s'est produite lors de l'API {api_url} : {e}")

        # Afficher un avertissement pour le décompte des objets traités
        logging.warning(f"{index}/{len(df_urls)} objets traités")

    return data

def main(input_file, output_file):
    try:
        # Lire le fichier Excel avec les URLs d'API
        df_urls = pd.read_excel(input_file, sheet_name='Feuil1')

        # Traiter les données
        data = process_data(df_urls)

        # Créez un nouveau classeur Excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Ajoutez les en-têtes des colonnes
        sheet.append(['dc:identifier', 'dc:relation', 'dc:source'])

        # Insérez les données dans le tableur
        for row in data:
            sheet.append(row)

        # Sauvegardez le fichier Excel
        workbook.save(output_file)

        print("Le traitement est terminé et les résultats sont sauvegardés dans", output_file)
    except Exception as e:
        print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilisation : python script_a_executer.py <fichier_entree.xlsx> <fichier_sortie.xlsx>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)