from tkinter import *




PRAZNO = "."
#zaenkrat bo velikost polja fikso določena
S=6
KOORDINATE=[]
IGRALEC_MODRI = "M"
IGRALEC_RDECI = "R"

def nasprotnik(igralec):
	"Vrne nasprotnika"
	if igralec == IGRALEC_MODRI:
		return IGRALEC_RDECI
	elif igralec == IGRALEC_RDECI:
		return IGRALEC_MODRI
	else:
		assert False, "neveljaven nasprotnik"

class Igra():

	def __init__(self):
		#za začetek bo igra na plošči 6x6
		#S (Size) bo vrednost, ki jo bo igralec imel možnost nastaviti v menuju z drsnikom
		#zaenkrat bo S fiksno določen
		self.plosca = [[PRAZNO for y in range(S)] for x in range(S)]
		#nastavi začetni poziciji
		self.plosca[S-1][0]= IGRALEC_MODRI
		self.plosca[0][S-1]= IGRALEC_RDECI
		self.na_potezi = IGRALEC_MODRI

	def naredi_potezo(self):
		#potrebuje dodatek za veljavnost poteze
		self.na_potezi = nasprotnik(self.na_potezi)

	def umesti_potezo(self, igralec, x, y):
		self.plosca[y][x] = igralec
		#začasno
		print (self.plosca)

	def veljavna_poteza(self, igralec, x, y):
		if self.plosca[y][x]==PRAZNO:
			#for i in range (-1,2):
			#	for j in range(-1,2):
			#		pl=self.plosca[y+i][x+j]
			#		if not i==0 and j==0:
			#			if pl==igralec:
			return True
		else:
			return False



class Gui():

	def __init__(self, root):
		
		#velikost okna se prilagaja velikosti polja
		self.plosca = Canvas(root, width=100*(S+1), height=100*(S+1))
		self.plosca.grid(row=0, column=0)

		self.narisi_crte()

		self.plosca.bind('<Button-1>', self.klik)
		#self.plosca.bind('<Button-1>', self.pobarvaj_modro)
		
		root.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(root))

		self.igra = Igra()


	def narisi_crte(self):
		"""Nariše črte igralnega polja"""
		#velikost majhnih kvadratkov se še ne prilagaja velikosti polja
		#dokler je velikost pola fiksno določena oz. max pribl. 8 to ni problem
		#potem bo treba za številčnejšo mrežo manjšati kvadratke
		mera=100*(S+1)
		for x in range (50, mera, 100):
			self.plosca.create_line(x, 50, x, mera-50)
		for y in range (50, mera, 100):
			self.plosca.create_line(50, y, mera-50, y)
		#pobarvaj začetni poziciji
		self.plosca.create_rectangle(100-49, 600-49, 100+49, 600+49, fill="blue")
		self.plosca.create_rectangle(600-49, 100-49, 600+49, 100+49, fill="red")

	def klik(self, event):
		"""Naredi preveč. V prihodnje je treba razdeliti njegovo delo v druge funkcije."""
		if 50<event.x<((S+1)*100-50) and 50<event.y<((S+1)*100-50):
			for i in range(1, S+1):
				KOORDINATE.append(100*i)

			x=min(KOORDINATE, key=lambda a:abs(a-event.x))
			y=min(KOORDINATE, key=lambda b:abs(b-event.y))

			xp=(x//100)-1
			yp=(y//100)-1

			if self.igra.veljavna_poteza(self.igra.na_potezi, xp, yp):

				if self.igra.na_potezi == IGRALEC_MODRI:
					self.pobarvaj_modro(x, y)
					self.igra.umesti_potezo(IGRALEC_MODRI, xp, yp)

				elif self.igra.na_potezi == IGRALEC_RDECI:
					self.pobarvaj_rdece(x, y)
					self.igra.umesti_potezo(IGRALEC_RDECI, xp, yp)

				self.igra.naredi_potezo()
			else: 
				print ("Zasedeno polje!")
		#začasno
		print ("Klik na {0}, {1}, x je {2}, y je {3}".format(event.x, event.y, x, y))
		

	def pobarvaj_modro(self, x, y):
		"""Pobarva polje na modro"""
		self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="blue")
		
		

	def pobarvaj_rdece(self, x, y):
		"""Pobarva polje na rdece"""
		self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="red")
		

	def zapri_okno(self, root):
		"""Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
		#Dejansko zapremo okno.
		root.destroy()






#manjka še on top "menu" okno
if __name__ == "__main__":

	root = Tk()
	root.title("SpaceMe")
	#manjkajo stavri, za katere ne vem kaj bodo počele
	aplikacija = Gui(root)

	root.mainloop()