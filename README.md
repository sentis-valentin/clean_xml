# clean_xml
Nettoyer les appels d'API Gallica SRU

# Contexte

Ces script sont fait dans le but de récupérer des cotes et liens pour enrichir un SIGB.
S'agissant d'une bibliothèque numérique Gallica Marque Blanche (GMB), l'usage de l'API de recherche Gallica permet cela.

Le tout se compose de 4 script : 

- app.py, contenant tout ce qu'il faut pour créer le fichier .exe pour Windows
- gui_app.py, permettant la création et l'utilisation de la fenêtre d'application (GUI)
- clean_xml.py, étant le script lancé en arrière-plan par gui_app.py
- main.py, le script à proprement dit
  
## main.py

Le script s'occupe de chercher l'url d'appel de l'API SRU de gallica ou d'une GMB dans un tableur Excel, ligne par ligne, puis recherche les balises XML (dans mon cas dc:identifier, dc:relation et dc:source).
Une fois les informations trouvées, le script les isncrits dans un nouveau tableur Excel, avec comme nom de colonne les balises recherchées.

Pour adapter le script, il faut changer le nom du fichier et son emplacement sur cette ligne :

`df_urls = pd.read_excel('**856_url_test.xlsx**', sheet_name='Feuil1')`


## Description
Il s'agit d'un fichier script et d'un fichier .exe pour profiter d'un GUI sur Windows.
Avant tout, sur un système Unix, avoir python puis installer les bibliothèques suivantes :

`pip install tk requests openpyxl pandas bs4`

Après cela, éxécuter le script dans le dossier contenant le fichier excel : 

`python3 main.py`

Une fois finit, le script indique `$ Les données ont été récupérées et enregistrées dans [...].xlsx.` où `[...]` est le nom du fichier indiqué dans le script.

Pour Windows, double-cliquer sur le fichier clean_xml.exe, une fenêtre s'ouvre, proposant de choisir 1) le tableur excel contenant les URL, 2) le nom et l'emplacement du fichier de sortie.
Une fois cela fait, cliquer sur _Lancer le script_.

![GUI](/GUI.png#center)

A la fin, un fichier _log.txt_ est créé.

## GUI Windows

Si vous voulez adapter le code, voici comment créer le fichier .exe.

Installer les dépendances :
`pip install pyinstaller`
, adaptez app.spec, puis : 
`pyinstaller app.spec`
