# Oppgave 1
# a
class Parti:
    def __init__(self, partikode : str, navn : str):
        self.partikode = partikode
        self.navn = navn
        self.valgår = []
    def skriv(self):
        valgårtext = ", ".join(self.valgår)
        if valgårtext:
            print(f"{self.navn} {self.partikode} valgår: {valgårtext}")
        else:
            print(f"{self.navn} {self.partikode}")

a=Parti('A','Arbeiderpartiet')
sv=Parti('SV','Sosialistisk Venstreparti')
rødt=Parti('RØDT','Rødt')
sp=Parti('SP','Senterpartiet')
krf=Parti('KRF','Kristelig Folkeparti')
v=Parti('V','Venstre')
h=Parti('H','Høyre')
frp=Parti('FRP','Fremskrittspartiet')
mdg=Parti('MDG','Miljøpartiet De Grønne')
nkp=Parti('NKP','Norges Kommunistiske Parti')

partier=[a,sv,rødt,sp,krf,v,h,frp,mdg,nkp]



# b
def partiNavn(partikode_input):
    for p in partier:
        if p.partikode == partikode_input:
            return p.navn
    return "ukjent parti"

# c
def partiKode(partinavn_input):
    for p in partier:
        if p.navn == partinavn_input:
            return p.partikode
    return "ukjent parti"

# d
class StemmeTall:
    def __init__(self, partikode : str, stemmer : int):
        self.partikode = partikode
        self.stemmer = stemmer
        self.merknader = []
    def skriv(self):
        merknad_tekst = " / ".join(self.merknader)
        print(f"{self.partikode}: {self.stemmer} {merknad_tekst}")
    def leggTilMerknad(self, ny_merknad):
        self.merknader.append(ny_merknad)
mdgStemmer = StemmeTall("MDG", 100)

valgresultat = {}
for parti in partier:
    valgresultat[parti.navn] = StemmeTall(parti.partikode, 100)
# e
def lesStemmer():
    stemmer = []
    for navn, stemme in stemmer.items():
        stemmer.append(f"Antall stemmer for {navn}: {stemme.stemmer}")
    return stemmer


def finnResultat(resultat, parti):
    return(resultat[parti].stemmer)

def flestStemmer(valgresultat,parti1,parti2):
    kode1=partiKode(parti1)
    kode2=partiKode(parti2)
    if 'ukjent parti' in [kode1,kode2]:
        return 'ukjent parti'
    stemmer1=finnResultat(valgresultat,kode1)
    stemmer2=finnResultat(valgresultat,kode2)
    if stemmer1==stemmer2:
        return f'{parti1} og {parti2} fikk like mange stemmer ({stemmer1})'
    elif stemmer1>stemmer2:
        return f'{parti1} fikk flest stemmer ({stemmer1})'
    else: 
        return f'{parti2} fikk flest stemmer ({stemmer2})'

# oppgave 2
def lesPartier():
    partier = []
    with open("./partier.txt", "r", encoding="utf-8") as partitxt:
        partier_fra_tekst = partitxt.readlines()
    for parti in partier_fra_tekst:
        kode, navn = parti.strip().split(",")
        partier.append(Parti(kode, navn))
    
    #[print(parti.skriv()) for parti in partier] 
    return partier
partier = lesPartier()

# oppgave 3
# a
def lesKretser():
    kretser = {}
    with open("kretser.txt", "r", encoding="utf-8") as fil:
        data = fil.readlines()
        for rad in data:
            nummer, navn = rad.strip().split(",")
            nummer = int(nummer)
            kretser[nummer] = navn
    return kretser
kretser = lesKretser()

# b
def kretsNr(navn : str):
    global kretser
    
    for nummer, krets in kretser.items():
        if krets == navn:
            return nummer
    return "ukjent krets"


# oppgave 4
# a og b
def lesValg(valgfil : str, årstall : int):
    global partier
    valg = {}
    with open(valgfil, "r", encoding="utf-8") as fil:
        data = fil.readlines()
        data.pop(0)
        settepartier = []
        for rad in data:
            nummer, parti_kode, stemmer = rad.strip().split(",")
            nummer = int(nummer)
            
            for parti in partier:
                if parti.partikode == parti_kode and parti not in settepartier:
                    parti.valgår.append(str(årstall))
                    settepartier.append(parti)
            if nummer in valg:
                valg[nummer].append(StemmeTall(parti_kode, int(stemmer)))
            else:

                valg[nummer] = [StemmeTall(parti_kode, int(stemmer))]
    # sorter?
    return valg


# DEL 2
valg13=lesValg('stemmer2013.txt',2013)
valg17=lesValg('stemmer2017.txt',2017)
valg21=lesValg('stemmer2021.txt',2021)
valg25=lesValg('stemmer2025.txt',2025)

# oppgave 5
def flyktigePartier():
    for parti in partier:
        if len(parti.valgår) == 1:
            parti.skriv()
#flyktigePartier()

# oppgave 6
def kretsResultat(valg, krets : str, parti : str):
    global kretser
    global partier
    # finn parti
    parti_objekt = None
    for temp_parti in partier:
        if parti in [temp_parti.partikode, temp_parti.navn]:
            parti_objekt = temp_parti
    if parti_objekt == None:
        return "ukjent parti"
    # finn krets
    krets_objekt = None
    for krets_item in kretser.items():
        if krets in krets_item:
            krets_objekt = krets_item
    if krets_objekt == None:
        return "ukjent krets"
    for stemmetall in valg[krets_objekt[0]]:
        if stemmetall.partikode == parti_objekt.partikode:
            return stemmetall.stemmer

#oppgave 7
def samlet(valg):

    samlet_fortegnelse = {}
    for krets in valg.values():

        for stemmetall in krets:
            partikode = stemmetall.partikode
            stemmer = stemmetall.stemmer
            if partikode in samlet_fortegnelse:
                samlet_fortegnelse[partikode] += stemmer
            else:
                samlet_fortegnelse[partikode] = stemmer
    return samlet_fortegnelse

# oppgave 8
def prosentFordeling(valg):
    stemmer = samlet(valg)
    stemme_sum = sum(stemmer.values())
    prosent_fortegnelse = {}
    for partikode, stemme in stemmer.items():
        prosent_fortegnelse[partikode] = round(stemme / stemme_sum * 100, 1) 
    return prosent_fortegnelse
#print(prosentFordeling(valg25))
def printKretsOversikt(valg_prosentfordeling, krets_data):
    for stemmetall in krets_data:
        print(f"{partiNavn(stemmetall.partikode)} fikk {stemmetall.stemmer} stemmer ({valg_prosentfordeling[stemmetall.partikode]}%)")
def kretsOversikt(valg):
    krets = input("Krets:")
    krets_nummer = kretsNr(krets)
    valg_prosentfordeling = prosentFordeling(valg)
    while krets != "slutt":
        printKretsOversikt(valg_prosentfordeling, valg[krets_nummer])
        krets = input("Krets:")
#kretsOversikt(valg21)

# oppgave 10
