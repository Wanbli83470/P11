from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
count = 10
class search_products():
	def dire(self):
		print("Hello")

def save_pdf(name="Fred"):

	pdf = canvas.Canvas('{}.pdf'.format(name))

	pdf.drawString(3*cm, 25*cm, u'Bienvenue {} vous avez enregistré {} produits'.format(name, count))
	pdf.line(3*cm,24.5*cm,18*cm,24.5*cm)
	pdf.drawString(3*cm, 23*cm, u'Un texte')

	pdf.save()