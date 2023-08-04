import requests
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
import time
import logging

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
