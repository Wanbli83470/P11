from program import search_products, save_pdf
from gi.repository import Gtk
from constants import *
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import pymysql.cursors

"""CONNECT TO THE DATABASE"""

try :
    connection = pymysql.connect(host=HOST, #variable in file constantes.py
                                     user=USER,
                                     password=PASSWORD,
                                     db=DB,
                                     charset='utf8mb4',
                                     port = PORT,
                                     cursorclass=pymysql.cursors.DictCursor)
    print("\n Connexion réussi à la BDD : {}".format(DB))
except :
    print("\n erreur de connexion")

# On crée notre fenêtre principale
window = Gtk.Window()

# On assigne un titre à la fenêtre
window.set_title('PyNutrition')

# On ajoute des marges

window.set_border_width(10)


# On crée les boutons
button_search = Gtk.Button(label='Search substitutes')  # Création d'un bouton 1
button_exit = Gtk.Button(label='Exit') # Création d'un bouton de sortie
button_save = Gtk.Button(label='Save') # Création d'un bouton de sauvegarde
button_cleaning = Gtk.Button(label='Cleaned my products') # Création d'un bouton de sauvegarde
button_display = Gtk.Button(label='View my products')
button_pdf = Gtk.Button(label='Export PDF')

# On Crée les formulaires
form_save_pdf = Gtk.Entry()
form_search = Gtk.Entry()

# On crée une grille
grid = Gtk.Grid()

# On Attache les éléments à la grille
grid.attach(button_search, 0, 1, 3, 1)  # Le bouton_1 se trouve en (0;0), prend 3 cases de large et une de haut
grid.attach(form_search, 0, 0, 3, 1)
grid.attach(button_cleaning, 0, 2, 1, 1)  # Le bouton_2 se trouve en (0;1), prend une case de large et 3 de haut
grid.attach(button_save, 0, 3, 1, 1)
grid.attach(button_display, 0, 4, 1, 1)
grid.attach(button_pdf, 0, 5, 1, 1)
grid.attach(form_save_pdf, 1, 5, 2, 1)
grid.attach(button_exit, 0, 6, 1, 1)

# On affiche la grille
window.add(grid)

# On réagis au click des boutons
button_search.connect('clicked', search_products.dire)
button_exit.connect('clicked', Gtk.main_quit)
button_pdf.connect('clicked', save_pdf)
# On affiche toute notre fenêtre
window.show_all()

# On indique que le si la fenêtre est supprimée, la boucle principale s'arrête
window.connect('delete-event', Gtk.main_quit)

# On paramètre l'affichage de la fenêtre :
Gtk.Grid.set_column_homogeneous(grid, True)
Gtk.Grid.set_row_homogeneous(grid, True)
Gtk.Grid.set_row_spacing(grid, 8)
# On lance la boucle principale
Gtk.main()
