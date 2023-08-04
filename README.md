# clean_xml
Nettoyer les appels d'API Gallica SRU 

# Contexte

Ces script sont fait dans le but de récupérer des cotes et liens pour enrichir un SIGB.
S'agissant d'une bibliothèque numérique Gallica Marque Blanche (GMB), l'usage de l'API de recherche Gallica permet cela.

Le tout se compose de 4 script : 

- app.py, contenant tout ce qu'il faut pour créer le fichier .exe pour Windows
- gui_app.py, permettant la création et l'utilisation de l'interface graphique (GUI)
- clean_xml.py, étant le script lancé en arrière-plan par gui_app.py
- main.py, le script à proprement dit
  
## main.py

Le script `main.py` recherche les URL d'appels de l'API SRU de Gallica ou d'une GMB dans un fichier Excel, ligne par ligne. Ensuite, il extrait les balises XML pertinentes (dans ce cas, les balises dc:identifier, dc:relation et dc:source). Une fois les informations trouvées, le script les inscrit dans un nouveau fichier Excel, avec les balises recherchées en tant que noms de colonnes.

Pour adapter le script à vos besoins, vous devez simplement changer le nom du fichier et son emplacement dans cette ligne :

`df_urls = pd.read_excel('856_url_test.xlsx', sheet_name='Feuil1')`

## Description

### prérequis

Il s'agit d'un fichier script et d'un fichier .exe pour profiter d'un GUI sur Windows.
Avant tout, sur un système Unix, avoir python puis installer les bibliothèques suivantes :

`pip install tk requests openpyxl pandas bs4`

### Exécution sur un système Unix

Après cela, éxécuter le script dans le dossier contenant le fichier excel : 

`python3 main.py`

Une fois finit, le script indique `$ Les données ont été récupérées et enregistrées dans [...].xlsx.` où `[...]` est le nom du fichier indiqué dans le script.

### Exécution sur Windows avec interface graphique (GUI)

Pour Windows, double-cliquer sur le fichier clean_xml.exe, une fenêtre s'ouvre, proposant de choisir 1) le tableur excel contenant les URL, 2) le nom et l'emplacement du fichier de sortie.
Une fois cela fait, cliquer sur _Lancer le script_.

![GUI](/GUI.png#center)

A la fin, un fichier _log.txt_ est créé.

Si vous voulez adapter le code, voici comment créer le fichier .exe.

Installer les dépendances :
`pip install pyinstaller`
, adaptez app.spec, puis : 
`pyinstaller app.spec`
