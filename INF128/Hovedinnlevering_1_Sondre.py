#Oppgave 1
#a
def størstMinusMinst(tall1, tall2):
    return max(tall1, tall2), min(tall1, tall2)
#b
def temperaturForskjell(område1, område2):
    temperatur1 = input(f"Temperatur {område1}: ")
    temperatur2 = input(f"Temperatur {område2}: ")
    print(f"Temperaturforskjellen mellom {område1} og {område2} er {størstMinusMinst(temperatur1, temperatur2)} grader")
#temperaturForskjell("London", "Paris")

#c
def absoluttverdi(tall1):
    return abs(tall1)
#Opggave 2
#a
def temperaturKonvertering(temperatur: float,måleenhet:str):
    print((temperatur-32)*5/9 if måleenhet == "F" else (temperatur *9/5 +32))
#temperaturKonvertering(20,"F")

#Oppgave 3

#a

class BankKonto:
    def __init__(self):
        self.saldo = 500
        self.rente = 0.01
        self.ordinærRente = 0.01
        self.bonusRente = 0.02
        self.nyRenteGrense = 1000000
        self.endringer = []
        
    def oppdater_siste_endringer(self, endring):
        self.endringer.append(endring)
        if len(self.endringer) > 3:
            self.endringer.pop(0)
            
    def oppdater_rentesats(self):
        if self.saldo >= self.nyRenteGrense:
            self.rente = self.bonusRente
            print("gratulerer du får bonusrente")
        elif self.rente == self.bonusRente:
            self.rente = self.ordinærRente
            print("du har nå ordinær rente")
            
    def vis_saldo(self):
        print(f"Saldo: {self.saldo}")

    def innskudd(self):
        beløp = int(input("beløp: "))
        self.saldo += beløp
        self.oppdater_siste_endringer(f"+{beløp}")

    def uttak(self):
        beløp = int(input("beløp: "))
        if beløp > self.saldo:
            print("overtrekk")
        else:
            self.saldo -= beløp
        self.oppdater_siste_endringer(f"-{beløp}")
        
    def renteoppgjør(self):
        saldoFør = self.saldo
        self.saldo *= (1 + self.rente)
        saldoEtter = self.saldo
        self.oppdater_siste_endringer(f"+{saldoEtter-saldoFør}")
        
    def vis_siste_endringer(self):
        if len(self.endringer) == 0:
            print("Ingen endringer enda.")
            return
        for endring in self.endringer:
            print(endring)
        
        

def velg():
    konto = BankKonto()
    brukerInput = ""
    #Få input
    while True:
        print(
        """
--------------------
1 - vis saldo
2 - innskudd
3 - uttak
4 - renteoppgjør
5 - siste endringer
stopp - stopper programmet
--------------------
        """)
        brukerInput = input("Velg handling:")
        if brukerInput == "1":
            konto.vis_saldo()
        elif brukerInput == "2":
            konto.innskudd()
        elif brukerInput == "3":
            konto.uttak()
        elif brukerInput == "4":
            konto.renteoppgjør()
        elif brukerInput == "5":
            konto.vis_siste_endringer()
        elif brukerInput == "stopp":
            return
        else:
            print("Input må være enten 1, 2, 3, 4 eller 5")
            velg()
        konto.oppdater_rentesats()

velg()
