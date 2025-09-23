#TODO oppdter sisteendringer og rentesats muligens feil.
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
        self.ny_rente = 0.02
        self.nyRenteGrense = 1000000
        self.endringer = []
    def oppdater_siste_endringer(self, endring):
        self.endringer.append(endring)
        if len(self.endringer) > 3:
            self.endringer.pop(0)
    def oppdater_rentesats(self):
        if self.saldo >= self.nyRenteGrense:
            self.rente = self.ny_rente
        if self.saldo < self.nyRenteGrense:
            self.rente = self.rente
    def vis_saldo(self):
        print(f"Saldo: {self.saldo}")

    def innskudd(self):
        beløp = int(input("beløp: "))
        self.saldo += beløp
        self.oppdater_siste_endringer(f"{beløp}")

    def uttak(self):
        beløp = int(input("beløp: "))
        if beløp > self.saldo:
            print("ikke dekning")
        else:
            self.saldo -= beløp
        self.oppdater_siste_endringer(f"-{beløp}")
        
    def renteoppgjør(self):
        self.saldo *= 1 + self.rente

    def vis_siste_endringer(self):
        print(self.endringer)
        
        

def velg():
    konto = BankKonto()
    brukerInput = ""
    #Få input
    while brukerInput != "stopp":
        print("""
    --------------------
    1 - vis saldo
    2 - innskudd
    3 - uttak
    4 - renteoppgjør
    5 - siste endringer
    --------------------""")
        brukerInput = input("Velg handling:")
    
    #print("Input må vær 1, 2, 3 eller 4")
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
        else:
            print("Input må være enten 1, 2, 3, 4 eller 5")
        konto.oppdater_rentesats()
velg()
