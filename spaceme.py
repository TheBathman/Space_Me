from tkinter import *




PRAZNO = "."
#zaenkrat bo velikost polja fikso določena
S=6
KOORDINATE=[]
IGRALEC_MODRI = "M"
IGRALEC_RDECI = "R"
seznam=[]

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

		self.gui=Gui

	def naredi_potezo(self, igralec, x, y):
		"""Metoda zavzame nasprotnikova polja in mu preda potezo"""
		self.plosca[y][x] = igralec
		seznam=[((x+1)*100,(y+1)*100)]
		for i in range (0,S):
			for j in range(0,S):
				if self.plosca[i][j]==nasprotnik(igralec):
					if -2<(y-i)<2:
						if -2<(x-j)<2:
							self.plosca[i][j]=igralec
							ip=(i+1)*100
							jp=(j+1)*100
							seznam.append((jp,ip))

		self.na_potezi = nasprotnik(self.na_potezi)
		print (self.plosca)
		return (seznam)

	def umesti_potezo(self, igralec, x, y):
		#self.plosca[y][x] = igralec
		#začasno
		#print (self.plosca)
		pass

	def veljavna_poteza(self, igralec, x, y):
		if self.plosca[y][x]==PRAZNO:
			for i in range (0,S):
				for j in range(0,S):
					if self.plosca[i][j]==igralec:
						if -2<(y-i)<2:
							if -2<(x-j)<2:
								return True
		else:
			return False

	def restart(self):
		self.plosca = [[PRAZNO for y in range(S)] for x in range(S)]
		
		self.plosca[S-1][0]= IGRALEC_MODRI
		self.plosca[0][S-1]= IGRALEC_RDECI
		
		self.na_potezi = IGRALEC_MODRI



class Gui():

	TAG_FIGURA = 'figura'

	def __init__(self, root):

		#velikost okna se prilagaja velikosti polja
		self.plosca = Canvas(root, width=100*(S+1), height=100*(S+1))
		self.plosca.grid(row=0, column=0)

		self.narisi_crte()

		self.plosca.bind('<Button-1>', self.klik)
				
		root.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(root))

		self.igra = Igra()

		#Glavni menu
		menu = Menu(root)
		root.config(menu=menu)
		menu_moznosti = Menu(menu)
		menu.add_cascade(label="Options", menu=menu_moznosti)
		menu_moznosti.add_command(label="Restart", command=lambda:self.restart())



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
					#self.igra.umesti_potezo(IGRALEC_MODRI, xp, yp)
					seznam=self.igra.naredi_potezo(IGRALEC_MODRI, xp, yp)
					self.pobarvaj_modro(seznam)

				elif self.igra.na_potezi == IGRALEC_RDECI:
					seznam=self.igra.naredi_potezo(IGRALEC_RDECI, xp, yp)
					self.pobarvaj_rdece(seznam)

				
			else: 
				print ("Zasedeno polje!")
		#začasno
		print ("Klik na {0}, {1}, x je {2}, y je {3}".format(event.x, event.y, x, y))
		

	def pobarvaj_modro(self, seznam):
		"""Pobarva polje na modro"""
		for i in range(len(seznam)):
			x=seznam[i][0]
			y=seznam[i][1]
			self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="blue", tag=Gui.TAG_FIGURA)
		
		

	def pobarvaj_rdece(self, seznam):
		"""Pobarva polje na rdece"""
		for i in range(len(seznam)):
			x=seznam[i][0]
			y=seznam[i][1]
			self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="red", tag=Gui.TAG_FIGURA)
		
	def restart(self):
		"""Metoda pobriše kvadratke"""
		self.plosca.delete(Gui.TAG_FIGURA)
		self.igra.restart()

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