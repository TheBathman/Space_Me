from tkinter import *




PRAZNO = "."
#zaenkrat bo velikost polja fikso določena
S=5
KOORDINATE=[]
IGRALEC_MODRI = "M"
IGRALEC_RDECI = "R"
seznam=[]
IGRLACA=[IGRALEC_MODRI,IGRALEC_RDECI]

def nasprotnik(igralec):
	"Vrne nasprotnika"
	if igralec == IGRALEC_MODRI:
		return IGRALEC_RDECI
	elif igralec == IGRALEC_RDECI:
		return IGRALEC_MODRI
	else:
		assert False, "neveljaven nasprotnik"

##########################################################################

class Igra():

	def __init__(self):
		#za začetek bo igra na plošči SxS
		#S (Size) bo vrednost, ki jo bo igralec imel možnost nastaviti v menuju z drsnikom
		#zaenkrat bo S fiksno določen
		self.plosca = [[PRAZNO for y in range(S)] for x in range(S)]
		#nastavi začetni poziciji
		self.plosca[S-1][0]= IGRALEC_MODRI
		self.plosca[0][S-1]= IGRALEC_RDECI
		self.na_potezi = IGRALEC_MODRI

	def naredi_potezo(self, x, y):
		"""Metoda zavzame nasprotnikova polja in mu preda potezo"""
		xp=(x//100)-1
		yp=(y//100)-1
		igralec = self.na_potezi
		self.plosca[yp][xp] = igralec
		seznam=[(xp,yp)]
		for i in range (0,S):
			for j in range(0,S):
				if self.plosca[i][j]==nasprotnik(igralec):
					if -2<(yp-i)<2:
						if -2<(xp-j)<2:
							self.plosca[i][j]=igralec
							seznam.append((j,i))

		self.na_potezi = nasprotnik(self.na_potezi)
		print (self.plosca)
		return (seznam)

	def sosedi(self, x, y):
		"""Metoda preveri, kateri so sosedi izbranega polja."""
		sosedi = []
		for (dx, dy) in ((-1,-1), (-1,0), (-1,1),
				 (0, -1),         (0, 1),
				 (1, -1), (1, 0), (1, 1)):
			if 0 <= x + dx < S and 0 <= y + dy < S:
				sosedi.append((x + dx, y + dy))
		#print ("Sosedi {0} so {1}".format((x,y), sosedi))
		return sosedi

	def veljavna_poteza(self, x, y):
		"""Metoda preverja ali je dana poteza veljavna."""
		xp=(x//100)-1
		yp=(y//100)-1
		if self.plosca[yp][xp] != PRAZNO:
			return False
		else:
			for (u, v) in self.sosedi(xp, yp):
				if self.plosca[v][u] == self.na_potezi:
					return True
			return False

	def veljavne_poteze(self):
		"""Metoda vrača seznam veljavnih potez."""
		return [(i,j) for i in range(S) for j in range(S) if 
				self.veljavna_poteza(100*(i+1), 100*(j+1))]

	def je_konec(self):
		"""Metoda vrne True če je igre konec."""
		return (len(self.veljavne_poteze()) == 0)

	def stanje(self):
		"Metoda na koncu igre preveri kdo je zmagal in s kakšnim rezultatom."
		steviloM=0
		steviloR=0
		for i in range(S):
			for j in range(S):
				if self.plosca[i][j]=='M':
					steviloM+=1
				elif self.plosca[i][j]=='R':
					steviloR+=1
		if steviloM < steviloR:
			zmagovalec = 'rdeči'
		elif steviloM > steviloR:
			zmagovalec = 'modri'
		elif steviloM == steviloR:
			zmagovalec = 'neodločeno'
		else:
			assert False, "Pri izračunu stanja je šlo nekaj narobe."
		
		return ((zmagovalec, steviloM, steviloR))

	def kopija(self):
		"""Vrne kopijo igre"""
		k = Igra()
		k.plosca = [self.plosca[i][:] for i in range(S)]
		k.na_potezi = self.na_potezi
		return k

################################################################################
class Clovek():
	 def __init__(self, gui):
	 	self.gui = gui

	 def igraj(self):
	 	pass

	 def klik(self, x, y):
	 	self.gui.naredi_potezo(x,y)

############################################################################

class Racunalnik():
	def __init__(self, gui, algoritem):
		self.gui = gui
		self.algoritem = algoritem

	def igraj(self):
		"""Zaenkrat odirga prvo veljavno potezo"""
		(x,y)=self.algoritem.izracunaj_potezo(self.gui.igra.kopija())
		self.gui.naredi_potezo(100*(x+1), 100*(y+1))


	def klik(self, x, y):
		pass
		
################################################################################

class Minimax():
	def __init__(self):
		#self.globina = globina
		self.igra = None
		self.igram = None
		self.poteza = None

	def izracunaj_potezo(self, igra):
		self.igra = igra
		x = self.igra.veljavne_poteze()[0][0]
		y = self.igra.veljavne_poteze()[0][1]
		return (x,y)	
		#self.igra = igra
		#self.igram = self.igra.na_potezi
		#self.poteza = None

	ZMAGA = 1000000
	NESKONCNO = ZMAGA + 1

	#def minimax(self, globina, maxiAliMini):


		#if self.igra.je_konec():




##############################################################################

class Gui():

	TAG_FIGURA = 'figura'

	def __init__(self, root):
		#velikost okna se prilagaja velikosti polja
		self.plosca = Canvas(root, width=100*(S+1), height=100*(S+1))
		self.plosca.grid(row=2, column=0)

		self.narisi_crte()

		self.plosca.bind('<Button-1>', self.klik)
				
		root.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(root))

		self.igralec_modri = None
		self.igralec_rdeci = None
		self.igra = None # Na začetku igre sploh ni, ker se nismo začeli

		#Glavni menu
		menu = Menu(root)
		root.config(menu=menu)
		menu_moznosti = Menu(menu)
		menu.add_cascade(label="Možnosti", menu=menu_moznosti)
		menu_moznosti.add_command(label="Človek proti človeku", command=lambda:
										self.restart(Clovek(self), Clovek(self)))
		menu_moznosti.add_command(label="Človek proti računalniku", command=lambda:
										self.restart(Clovek(self), Racunalnik(self, Minimax())))
		menu_moznosti.add_command(label="Računalnik proti računalniku", command=lambda:
										self.restart(Racunalnik(self, Minimax()), Racunalnik(self)))
		menu_moznosti.add_command(label="Računalnik proti človeku", command=lambda:
										self.restart(Racunalnik(self, Minimax()), Clovek(self)))

		self.napis1 = StringVar(root, value="Space Me!")
		Label(root, textvariable=self.napis1).grid(row=0, column=0)

		self.napis2 = StringVar(root, value="Na potezi je modri.")
		Label(root, textvariable=self.napis2).grid(row=1, column=0)

		self.restart(Clovek(self), Racunalnik(self, Minimax()))

	def narisi_crte(self):
		"""Nariše črte igralnega polja"""
		#velikost majhnih kvadratkov se še ne prilagaja velikosti polja
		#dokler je velikost pola fiksno določena oz. max pribl. 8 to ni problem
		#potem bo treba za številčnejšo mrežo manjšati kvadratke
		mera=100*(S+1)
		for i in range(0, S+1):
			self.plosca.create_line(50 + 100 * i, 50, 50 + 100 * i, 100 * (S + 1) - 50)
		# for x in range (50, mera, 100):
		# 	self.plosca.create_line(x, 50, x, mera-50)
		for y in range (50, mera, 100):
			self.plosca.create_line(50, y, mera-50, y)

	def klik(self, event):
		"""Pretvori klik v koordinate."""
		if 50<event.x<((S+1)*100-50) and 50<event.y<((S+1)*100-50):
			for i in range(1, S+1):
				KOORDINATE.append(100*i)

			x=min(KOORDINATE, key=lambda a:abs(a-event.x))
			y=min(KOORDINATE, key=lambda b:abs(b-event.y))
			
			if not self.igra.veljavna_poteza(x, y):
				print ("Neveljavna poteza")
			else:
				if self.igra.na_potezi == IGRALEC_MODRI:
					self.igralec_modri.klik(x,y)
				
				elif self.igra.na_potezi == IGRALEC_RDECI:
					self.igralec_rdeci.klik(x,y)
					
				else:
					assert False, "Nisem se zmotil, to se ne bo zgodilo"
			#začasno
			print ("Klik na {0}, {1}, x je {2}, y je {3}".format(event.x, event.y, x, y))
		else:
			pass

	def naredi_potezo(self, x, y):
		"""Metoda naredi potezo in spremeni napis o stanju"""
		if self.igra.na_potezi == IGRALEC_MODRI:
			seznam=self.igra.naredi_potezo(x, y)
			self.pobarvaj_modro(seznam)

		elif self.igra.na_potezi == IGRALEC_RDECI:
			seznam=self.igra.naredi_potezo(x, y)
			self.pobarvaj_rdece(seznam)

		else:
			assert False, "Nisem se zmotil, to se ne bo zgodilo"

		if self.igra.je_konec():
			self.konec()
		elif self.igra.na_potezi == IGRALEC_MODRI:
			self.napis2.set("Na potezi je modri.")
			self.igralec_modri.igraj()
		elif self.igra.na_potezi == IGRALEC_RDECI:
			self.napis2.set("Na potezi je rdeči.")
			self.igralec_rdeci.igraj()
		else:
			assert False, "Nan se nikoli ne zmoti"

	def pobarvaj_modro(self, seznam):
		"""Pobarva polje na modro"""
		for i in range(len(seznam)):
			(x,y) = seznam[i]
			x = 100 * (x + 1)
			y = 100 * (y + 1)
			self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="blue", tag=Gui.TAG_FIGURA)
		
	def pobarvaj_rdece(self, seznam):
		"""Pobarva polje na rdece"""
		for i in range(len(seznam)):
			x = 100 * (seznam[i][0] + 1)
			y = 100 * (seznam[i][1] + 1)
			self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="red", tag=Gui.TAG_FIGURA)
		
	def restart(self, igralec_modri, igralec_rdeci):
		"""Metoda ponastavi igro"""
		self.plosca.delete(Gui.TAG_FIGURA)
		#pobarvaj začetni poziciji
		self.pobarvaj_modro([(0,S-1)])
		self.pobarvaj_rdece([(S-1,0)])
		self.napis1.set("Space Me!")
		self.napis2.set("Na potezi je modri.")
		self.igra = Igra()

		self.igralec_modri = igralec_modri
		self.igralec_rdeci = igralec_rdeci
		self.igralec_modri.igraj()

	def zapri_okno(self, root):
		"""Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
		#Dejansko zapremo okno.
		root.destroy()

	def konec(self):
		"""Izpiše zmagovalca in rezultat."""
		self.napis1.set("Konec!")
		stanje=self.igra.stanje()
		if stanje[0]=='neodločeno':
			self.napis2.set("Igra je neodločena!")
		else:
			self.napis2.set("Zmagal je {0} s {1} proti {2}.".format(stanje[0], stanje[1], stanje[2]))
		
			

############################################################################################		


#manjka še on top "menu" okno
if __name__ == "__main__":

	root = Tk()
	root.title("SpaceMe")
	#manjkajo stavri, za katere ne vem kaj bodo počele
	aplikacija = Gui(root)

	root.mainloop()
