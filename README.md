# clean_xml
Nettoyer les appels d'API Gallica SRU

## Description
Il s'agit d'un fichier script et d'un fichier .exe pour profiter d'un GUI sur Windows.
Avant tout, sur un système Unix, avoir python puis installer les bibliothèques suivantes :

`pip install requests openpyxl pandas bs4`

Après cela, éxécuter le script dans le dossier contenant le fichier excel : 

`python3 main.py`

Une fois finit, le script indique `$ Les données ont été récupérées et enregistrées dans [...].xlsx.` où `[...]` est le nom du fichier indiqué dans le script.

Pour Windows, double-cliquer sur le fichier clean_xml.exe, une fenêtre s'ouvre, proposant de choisir 1) le tableur excel contenant les URL, 2) le nom et l'emplacement du fichier de sortie.
Une fois cela fait, cliquer sur _Lancer le script_.

![GUI](/GUI.png)

A la fin, un fichier _log.txt_ est créé.
