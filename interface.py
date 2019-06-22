from program import search_products
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
count = 10

def save_pdf(name="Fred"):

	#On récupère le nom du formulaire
	name_pdf = form_save_pdf.get_text()
	#On vide le formulaire
	form_save_pdf.set_text('')


	pdf = canvas.Canvas("{}.pdf".format(name_pdf))

	pdf.drawString(3*cm, 28*cm, u'Bienvenue {} vous avez enregistré {} produits'.format(name, count))
	pdf.line(10.5*cm,23*cm,10.5*cm,0*cm)
	#Create the column
	pdf.drawString(3.5*cm, 23.5*cm, u'Mes habitudes')
	pdf.drawString(13.5*cm, 23.5*cm, u'Mes substituts')
	#Create the lines
	nb_line = 21
	x = 21
	y = 21

	#Get the input_product from table SUBSTITUTS from Database
	with connection :
		cur = connection.cursor()
		cur.execute("SELECT INPUT_PRODUCT, PRODUIT_ID FROM SUBSTITUTS")
		data_sub = cur.fetchall()
	

	position = 20.4
	for s in data_sub :
		print(s["INPUT_PRODUCT"])
		print(s["PRODUIT_ID"])

		with connection :
			cur = connection.cursor()
			cur.execute("SELECT NOM FROM PRODUITS WHERE ID=%s" % (int(s["PRODUIT_ID"])))
			data_sub2 = cur.fetchall()
			pdf.drawString(14*cm, position*cm, str(data_sub2[0]["NOM"]))


		print(position)
		pdf.drawString(4*cm, position*cm, s["INPUT_PRODUCT"])
		pdf.line(0*cm,x*cm,21*cm,y*cm)
		nb_line = nb_line - 1
		position = position - 1
		x = x - 1
		y = y - 1

	#Get the substituts from table SUBSTITUS from Database


	pdf.save()

def cleaning_table(a="b"):
	"""CLEANING TABLES"""

	with connection.cursor() as cursor:
		sql = "DELETE FROM `SUBSTITUTS`;"
		cursor.execute(sql, ())
		connection.commit()

def windows_data(button):
	sub_window = Gtk.Window()
	
	sub_window.set_border_width(10) # Bordure

	# On recupère nos substituts
	with connection :
		cur = connection.cursor()
		cur.execute("SELECT INPUT_PRODUCT FROM SUBSTITUTS")
		data_sub = cur.fetchall()
		data_sub = str(data_sub)
		data_sub = data_sub.replace(',', '\n\n')

	# On affiche nos substituts
	label = Gtk.Label(data_sub)
	grid_data = Gtk.Grid()
	grid_data.attach(label, 0, 1, 1, 1)
	sub_window.add(grid_data)

	sub_window.show_all()

# On crée les boutons
button_search = Gtk.Button(label='Search substitutes')  # Création d'un bouton 1
button_exit = Gtk.Button(label='Exit') # Création d'un bouton de sortie
button_save = Gtk.Button(label='Save') # Création d'un bouton de sauvegarde
button_cleaning = Gtk.Button(label='Cleaned my substituts') # Création d'un bouton de sauvegarde
button_display = Gtk.Button(label='View my products')
button_pdf = Gtk.Button(label='Export PDF')

# On Crée les formulaires
form_save_pdf = Gtk.Entry()
form_search = Gtk.Entry()
# On crée une grille
grid = Gtk.Grid()

# On Attache les éléments à la grille
grid.attach(button_search, 0, 1, 3, 1)
grid.attach(form_search, 0, 0, 3, 1)
grid.attach(button_save, 0, 3, 1, 1)
grid.attach(button_display, 0, 4, 1, 1)
grid.attach(button_pdf, 0, 5, 1, 1)
grid.attach(form_save_pdf, 1, 5, 2, 1)
grid.attach(button_cleaning, 0, 6, 2, 1)

grid.attach(button_exit, 3, 6, 1, 1)

# On affiche la grille
window.add(grid)

# On réagis au click des boutons
button_search.connect('clicked', search_products.dire)
button_exit.connect('clicked', Gtk.main_quit)
button_pdf.connect('clicked', save_pdf)
button_cleaning.connect('clicked', cleaning_table)
button_display.connect('clicked', windows_data)
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
