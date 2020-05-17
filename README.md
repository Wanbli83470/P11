P11_ESTIVAL_THOMAS
=================

Program Installation Guide :
----------------------------

1. Download the Git hub repositories with "git clone https://github.com/Wanbli83470/P11_ESTIVAL_THOMAS" in your terminal or download the zip.
2. Install Python on your computer.
3. Enter the downloaded folder and activate the virtual environment using the following command: "./venv/bin/activate"
4. Install the necessary modules with: "pip install -r requirements.txt"
5. Launch the script "P11_08_create_bdd" in a mySql client or on the web interface "PhpMyAdmin"
6. Configure your login details in the "P11_02_constantes.py" file
7. Start the program with the following command: "P11_01_codesource.py"

Guide d'installation du programme :
----------------------------------

1. Télécharger le repositories Git hub à l'aide d'un "git clone https://github.com/Wanbli83470/P11_ESTIVAL_THOMAS" dans votre terminal ou bien en téléchargeant le zip.
2. Installer Python sur votre machine s'il ne l'est pas.
3. Entrer dans le dossier téléchargé et activez l'environnement virtuel à l'aide de la commande suivante : "./venv/bin/activate"
4. Installer les paquets et les dépendances à l'aide de la commande "pip install -r requirements.txt"
5. Lancer le script "P11_08_create_bdd" dans un client mySql ou bien sur l'interface web "PhpMyAdmin"
6. Configurer vos identifiants de connexion dans le fichier "P11_02_constantes.py"
7. Lancer le programme avec la commande suivante : "P11_01_codesource.py"


Launching of the test:
----------------------
1. Open a terminal in the root folder "P11_ESTIVAL_THOMAS"
2. Activate your virtual environment with command "./venv/bin/activate".
3. Lauch the commande "Python -m unittest"

Lancement des test :
--------------------
1. Ouvrir un terminal dans le dossier racine "P11_ESTIVAL_THOMAS"
2. Activez l'environnement virtuel à l'aide de la commande suivante : "./venv/bin/activate"
3. Lancer la commande : "python -m unittest"


Configure automatic updates (Linux / Ubuntu environment):
---------------------------------------
1. Open the file P11_09_update.sh and modify the absolute path with your username
2. Modify your crontab file on the command line with "crontab -e" by inserting a line like the following at the end of the file:
> - * * * * * bash /home/thomas/Bureau/P11_ESTIVAL_THOMAS/P11_09_update.sh


Paramétrer les mise à jour automatique (Environnement linux/Ubuntu) :
---------------------------------------
1. Ouvrir le fichier P11_09_update.sh et modifier le chemin absolu avec votre nom d'utilisateur
2. Modifier votre fichier crontab en ligne de commande avec "crontab -e" en insérant une ligne tel que la suivante en fin de fichier :
> - * * * * * bash /home/thomas/Bureau/P11_ESTIVAL_THOMAS/P11_09_update.sh
