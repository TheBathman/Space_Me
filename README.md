#Osnovne informacije:
* Igra se na kvadratni n x n mreži (n>4).
* Igro igrata dva igralca, križec X in krožec O.
* Cilj je zasesti čim večjo površino.
* Igra se konča, ko prvemu igralcu zmanka potez.
* Igro začne X.

#Potek:
  * Igralca začneta v nasprotnih vogalih mreže vsak s svojim pobarvanim kvadratkom
  * Igralec zasede eno od sosednjih polj (pobarva s svojo barvo)
  * Če igralec zasede polje, ki meji na nasprotnikova, postanejo tudi ta njegova
  * Igra poteka izmenično, igralec na vrsti opravi eno potezo
  
##Primer prvih nekaj potez:
###Začetna postavitev:
    +---+---+---+---+
    | X |   |   |   | 
    +---+---+---+---+
    |   |   |   |   |
    +---+---+---+---+
    |   |   |   |   |
    +---+---+---+---+
    |   |   |   | O | 
    +---+---+---+---+
   

###Prva poteza:
    +---+---+---+---+
    | X | X |   |   | 
    +---+---+---+---+
    |   |   |   |   |
    +---+---+---+---+
    |   |   |   |   |
    +---+---+---+---+
    |   |   |   | O | 
    +---+---+---+---+


###Druga poteza:
    +---+---+---+---+
    | X | X |   |   | 
    +---+---+---+---+
    |   |   |   |   |
    +---+---+---+---+
    |   |   | O |   |
    +---+---+---+---+
    |   |   |   | O | 
    +---+---+---+---+

###Tretja poteza:
    +---+---+---+---+
    | X | X | X |   | 
    +---+---+---+---+
    |   |   |   |   |
    +---+---+---+---+
    |   |   | O |   |
    +---+---+---+---+
    |   |   |   | O | 
    +---+---+---+---+

###Četrta poteza:
    +---+---+---+---+
    | O | O | O |   | 
    +---+---+---+---+
    |   | O |   |   |
    +---+---+---+---+
    |   |   | O |   |
    +---+---+---+---+
    |   |   |   | O | 
    +---+---+---+---+
 Krogec zavzame vsa sosednja polja in zmaga.
