from tkinter import *
import threading
import logging



PRAZNO = "."
#zaenkrat bo velikost polja fikso določena
S=6

IGRALEC_MODRI = "M"
IGRALEC_RDECI = "R"
NEODLOCENO = "neodloceno"
seznam=[]
IGRLACA=[IGRALEC_MODRI,IGRALEC_RDECI]
MINIMAX_GLOBINA=5


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
        self.plosca = [[PRAZNO for x in range(S)] for y in range(S)]
        #nastavi začetni poziciji
        self.plosca[S-1][0]= IGRALEC_MODRI
        self.plosca[0][S-1]= IGRALEC_RDECI
        self.na_potezi = IGRALEC_MODRI
        self.zgodovina = []

    def naredi_potezo(self, y, x):
        """Metoda zavzame nasprotnikova polja in mu preda potezo"""
        igralec = self.na_potezi
        self.plosca[y][x] = igralec
        seznam=[(y,x)]
        for vrstica in range (0,S):
            for stolpec in range(0,S):
                if self.plosca[vrstica][stolpec]==nasprotnik(igralec):
                    if -2<(y-vrstica)<2:
                        if -2<(x-stolpec)<2:
                            self.plosca[vrstica][stolpec]=igralec
                            seznam.append((vrstica, stolpec))

        self.na_potezi = nasprotnik(self.na_potezi)
        #logging.debug (self.plosca)
        return (seznam)

    def sosedi(self, y, x):
        """Metoda preveri, kateri so sosedi izbranega polja."""
        sosedi = []
        for (dy, dx) in ((-1,-1), (-1,0), (-1,1),
                 (0, -1),     (0, 1),
                 (1, -1), (1, 0), (1, 1)):
            if 0 <= x + dx < S and 0 <= y + dy < S:
                sosedi.append((y + dy, x + dx))
        # print ("Sosedi od ({0}, {1}) so {2}".format(y,x,sosedi))
        return sosedi

    def veljavna_poteza(self, y, x):
        """Metoda preverja ali je dana poteza veljavna."""
        if self.plosca[y][x] != PRAZNO:
            return False
        else:
            for (vrstica, stolpec) in self.sosedi(y, x):
                if self.plosca[vrstica][stolpec] == self.na_potezi:
                    return True
            return False

    def veljavne_poteze(self):
        """Metoda vrača seznam veljavnih potez."""
        poteze = [(vr,st) for vr in range(S) for st in range(S) if self.veljavna_poteza(vr, st)]
        # print ("*" * 50)
        # print ("POZICIJA ({0}):\n{1}".format(
        #     self.na_potezi,
        #     "\n".join(["".join(v) for v in self.plosca])))
        # print ("VELJAVNE: {0}".format(poteze))
        # print ("*" * 50)
        return poteze

    def je_konec(self):
        """Metoda vrne True če je igre konec."""
        return (len(self.veljavne_poteze()) == 0)

    def stanje(self):
        "Metoda na koncu igre preveri kdo je zmagal in s kakšnim rezultatom."
        steviloM=0
        steviloR=0
        for vr in range(S):
            for st in range(S):
                if self.plosca[vr][st]=='M':
                    steviloM+=1
                elif self.plosca[vr][st]=='R':
                    steviloR+=1
        if steviloM < steviloR:
            zmagovalec = IGRALEC_RDECI
        elif steviloM > steviloR:
            zmagovalec = IGRALEC_MODRI
        elif steviloM == steviloR:
            zmagovalec = NEODLOCENO
        else:
            assert False, "Pri izračunu stanja je šlo nekaj narobe."
        
        return (steviloM, steviloR, zmagovalec)

    def kopija(self):
        """Vrne kopijo igre"""
        k = Igra()
        k.plosca = [self.plosca[vr][:] for vr in range(S)]
        k.na_potezi = self.na_potezi
        return k

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo."""
        p = [self.plosca[vr][:] for vr in range(S)]
        self.zgodovina.append((p, self.na_potezi))

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca, self.na_potezi) = self.zgodovina.pop()

################################################################################
class Clovek():
     def __init__(self, gui):
         self.gui = gui

     def igraj(self):
         pass
     def prekini(self):
         pass

     def klik(self, vr, st):
         self.gui.naredi_potezo(vr, st)

############################################################################

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem
        self.mislec = None

    def igraj(self):
        """Zaenkrat odirga prvo veljavno potezo"""
        self.mislec = threading.Thread(target=lambda:
                    self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))
        self.mislec.start()
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        if self.algoritem.poteza is not None:
            (vr, st)=self.algoritem.poteza
            self.gui.naredi_potezo(vr, st)
            logging.debug ("minimax je izračunal vr={0} st={1}".format(vr,st))
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        if self.mislec:
            self.algoritem.prekini()
            self.mislec.join()
            self.mislec = None


    def klik(self, vr, st):
        pass
        
###############################################################
class Minimax():
    def __init__(self, globina):
        self.globina = globina
        self.igra = None
        self.igram = None
        self.poteza = None
        self.prekinitev = None

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.igram = self.igra.na_potezi
        self.poteza = None
        self.prekinitev = False

        (poteza, vrednost) = self.minimax(self.globina, True)
        self.igra = None
        self.igram = None

        if not self.prekinitev:
            print ("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            return poteza

    ZMAGA = 1000000
    NESKONCNO = ZMAGA + 1

    def minimax(self, globina, maksimiziramo):
        if self.prekinitev:
            logging.debug ("Minimax prekinja.")
            return (None, 0)
        if self.igra.je_konec():
            stanje = self.igra.stanje()
            zmagovalec = stanje[2]
            if zmagovalec == self.igram:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.igram):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        else:
            if globina == 0:
                vrednost = self.vrednost_pozicije()
                return (None, vrednost)
            else:
                if maksimiziramo:
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for poteza in self.igra.veljavne_poteze():
                        self.igra.shrani_pozicijo()
                        self.igra.naredi_potezo(poteza[0], poteza[1])
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                else:
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for poteza in self.igra.veljavne_poteze():
                        self.igra.shrani_pozicijo()
                        self.igra.naredi_potezo(poteza[0], poteza[1])
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                if globina >= MINIMAX_GLOBINA - 2:
                    print (("---" * (MINIMAX_GLOBINA - globina)) + 
                           "{0}: poteza={1}, vrednost={2}, max={3}".format(
                               globina, najboljsa_poteza, vrednost_najboljse, maksimiziramo))
                return (najboljsa_poteza, vrednost_najboljse)

    def vrednost_pozicije(self):
        vrednost = 0
        stM=0
        stR=0
        for vr in range(S):
            for st in range(S):
                if self.igra.plosca[vr][st]=='M':
                    stM+=1
                elif self.igra.plosca[vr][st]=='R':
                    stR+=1
        if self.igram == IGRALEC_MODRI:
            vrednost = (stM-stR)
            return vrednost
        elif self.igram == IGRALEC_RDECI:
            vrednost = (stR-stM)
            return vrednost
        else:
            assert False, "Vrednost pozicij ima neveljavnega igralca."


##############################################################################
class AlfaBeta():

    ZMAGA = 1000000
    NESKONCNO = ZMAGA + 1

    def __init__(self, globina):
        self.globina = globina
        self.igra = None
        self.igram = None
        self.poteza = None
        self.prekinitev = None

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.igram = self.igra.na_potezi
        self.poteza = None
        self.prekinitev = False

        (poteza, vrednost) = self.alfabeta(self.globina, -AlfaBeta.NESKONCNO, AlfaBeta.NESKONCNO, True)
        self.igra = None
        self.igram = None

        if not self.prekinitev:
            print ("alfabeta: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            return poteza

    def vrednost_pozicije(self):
        vrednost = 0
        stM=0
        stR=0
        for vr in range(S):
            for st in range(S):
                if self.igra.plosca[vr][st]=='M':
                    stM+=1
                elif self.igra.plosca[vr][st]=='R':
                    stR+=1
        if self.igram == IGRALEC_MODRI:
            vrednost = (stM-stR)
            return vrednost
        elif self.igram == IGRALEC_RDECI:
            vrednost = (stR-stM)
            return vrednost
        else:
            assert False, "Vrednost pozicije ima neveljavnega igralca."

    def alfabeta(self, globina, alfa, beta, maksimiziramo):
        """Optimiziran minimax. """
        if self.prekinitev:
            logging.debug ("Alfabeta prekinja.")
            return (None, 0)
        if self.igra.je_konec():
            stanje = self.igra.stanje()
            zmagovalec = stanje[2]
            if zmagovalec == self.igram:
                return (None, AlfaBeta.ZMAGA)
            elif zmagovalec == nasprotnik(self.igram):
                return (None, -AlfaBeta.ZMAGA)
            else:
                return (None, 0)
        else:
            if globina == 0:
                vrednost = self.vrednost_pozicije()
                return (None, vrednost)
            else:
                if maksimiziramo:
                    najboljsa_poteza = None
                    #vrednost_najboljse = -Minimax.NESKONCNO
                    for poteza in self.igra.veljavne_poteze():
                        self.igra.shrani_pozicijo()
                        self.igra.naredi_potezo(poteza[0], poteza[1])
                        vrednost = self.alfabeta(globina-1, alfa, beta, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > alfa:
                            alfa = vrednost
                            najboljsa_poteza = poteza
                        if alfa >= beta:
                            break
                    return (najboljsa_poteza, alfa)

                else:
                    najboljsa_poteza = None
                    #vrednost_najboljse = Minimax.NESKONCNO
                    for poteza in self.igra.veljavne_poteze():
                        self.igra.shrani_pozicijo()
                        self.igra.naredi_potezo(poteza[0], poteza[1])
                        vrednost = self.alfabeta(globina-1, alfa, beta, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < beta:
                            beta = vrednost
                            najboljsa_poteza = poteza
                        if alfa >= beta:
                            break
                    return (najboljsa_poteza, beta)

                assert (najboljsa_poteza is not None), "alfabeta: izračunana poteza je None"
                #return (najboljsa_poteza, vrednost_najboljse)




##############################################################################

class Gui():

    TAG_FIGURA = 'figura'

    def __init__(self, root, globina):
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
                                        self.restart(Clovek(self), Racunalnik(self, AlfaBeta(globina))))
        menu_moznosti.add_command(label="Računalnik proti računalniku", command=lambda:
                                        self.restart(Racunalnik(self, AlfaBeta(globina)), Racunalnik(self, AlfaBeta(globina))))
        menu_moznosti.add_command(label="Računalnik proti človeku", command=lambda:
                                        self.restart(Racunalnik(self, AlfaBeta(globina)), Clovek(self)))

        self.napis1 = StringVar(root, value="Space Me!")
        Label(root, textvariable=self.napis1).grid(row=0, column=0)

        self.napis2 = StringVar(root, value="Na potezi je modri.")
        Label(root, textvariable=self.napis2).grid(row=1, column=0)

        self.restart(Clovek(self), Racunalnik(self, AlfaBeta(globina)))

    def narisi_crte(self):
        """Nariše črte igralnega polja"""
        #velikost majhnih kvadratkov se še ne prilagaja velikosti polja
        #dokler je velikost pola fiksno določena oz. max pribl. 8 to ni problem
        #potem bo treba za številčnejšo mrežo manjšati kvadratke
        mera=100*(S+1)
        for i in range(0, S+1):
            self.plosca.create_line(50 + 100 * i, 50, 50 + 100 * i, 100 * (S + 1) - 50)
        # for x in range (50, mera, 100):
        #     self.plosca.create_line(x, 50, x, mera-50)
        for y in range (50, mera, 100):
            self.plosca.create_line(50, y, mera-50, y)

    def klik(self, event):
        """Pretvori klik v koordinate."""
        st = (event.x - 50) // 100
        vr = (event.y - 50) // 100
        # print ("Klik na ({0}, {1}), vr je {2}, st je {3}".format(event.x, event.y, vr, st))
        if 0 <= st < S and 0 <= vr < S and self.igra.veljavna_poteza(vr, st):
            if self.igra.na_potezi == IGRALEC_MODRI:
                self.igralec_modri.klik(vr,st)
                
            elif self.igra.na_potezi == IGRALEC_RDECI:
                self.igralec_rdeci.klik(vr,st)
                    
            else:
                assert False, "Nisem se zmotil, to se ne bo zgodilo"

    def naredi_potezo(self, vr, st):
        """Metoda naredi potezo in spremeni napis o stanju"""
        if self.igra.na_potezi == IGRALEC_MODRI:
            seznam=self.igra.naredi_potezo(vr, st)
            self.pobarvaj_modro(seznam)

        elif self.igra.na_potezi == IGRALEC_RDECI:
            seznam=self.igra.naredi_potezo(vr, st)
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
        for (vr,st) in seznam:
            x = 100 * (st + 1)
            y = 100 * (vr + 1)
            # print ("Barvam modro vr={0}, st={1}, (x,y) = {2}".format(vr,st,(x,y)))
            self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="blue", tag=Gui.TAG_FIGURA)
        
    def pobarvaj_rdece(self, seznam):
        """Pobarva polje na rdece"""
        for (vr,st) in seznam:
            x = 100 * (st + 1)
            y = 100 * (vr + 1)
            # print ("Barvam rdece vr={0}, st={1}, (x,y) = {2}".format(vr,st,(x,y)))
            self.plosca.create_rectangle(x-49, y-49, x+49, y+49, fill="red", tag=Gui.TAG_FIGURA)
        
    def restart(self, igralec_modri, igralec_rdeci):
        """Metoda ponastavi igro"""
        self.prekini_igralce()
        self.plosca.delete(Gui.TAG_FIGURA)
        #pobarvaj začetni poziciji
        self.pobarvaj_modro([(S-1,0)])
        self.pobarvaj_rdece([(0,S-1)])
        self.napis1.set("Space Me!")
        self.napis2.set("Na potezi je modri.")
        self.igra = Igra()

        self.igralec_modri = igralec_modri
        self.igralec_rdeci = igralec_rdeci
        self.igralec_modri.igraj()

    def prekini_igralce(self):
        if self.igralec_modri:
            self.igralec_modri.prekini()
        if self.igralec_rdeci:
            self.igralec_rdeci.prekini()

    def zapri_okno(self, root):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        self.prekini_igralce()
        #Dejansko zapremo okno.
        root.destroy()

    def konec(self):
        """Izpiše zmagovalca in rezultat."""
        self.napis1.set("Konec!")
        stanje=self.igra.stanje()
        if stanje[0]>stanje[1]:
            self.napis2.set("Zmagal je modri s {0} proti {1}.".format(stanje[0], stanje[1]))
        elif stanje[0]<stanje[1]:
            self.napis2.set("Zmagal je rdeči s {1} proti {0}.".format(stanje[0], stanje[1]))
        else:
            self.napis2.set("Igra je neodločena!")
        
            

############################################################################################        


#manjka še on top "menu" okno
if __name__ == "__main__":

    root = Tk()
    root.title("SpaceMe")
    #manjkajo stavri, za katere ne vem kaj bodo počele
    aplikacija = Gui(root, MINIMAX_GLOBINA)

    root.mainloop()
