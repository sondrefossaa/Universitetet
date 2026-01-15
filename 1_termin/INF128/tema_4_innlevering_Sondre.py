# Oppgave 1
# For løkke
def fakF(tall : int):
    if tall < 1:
        return
    sum = 1
    for i in range(2, tall+1):
        sum *= i
    return sum
# While løkke
def fakW(tall: int):
    if tall < 1:
        return
    sum = 1
    while tall > 1:
       sum *= tall
       tall -= 1
    return sum

# Oppgave 2
class Monark:
    def __init__(self, nasjon, navn, fra):
        self.nasjon = nasjon
        self.navn = navn
        self.fra = fra
        self.etterfølger = None
    def skriv(self):
        print(f"{self.navn} av {self.nasjon}, tilrådt: {self.fra}")
    def settEtterfølger(self, neste):
        self.etterfølger = neste

haakon = Monark("Norge","Kong Haakon VII", 1905)
olav = Monark("Norge","Kong Olav V", 1957)
haakon.settEtterfølger(olav)
harald = Monark("Norge","Kong Harald V", 1991)
olav.settEtterfølger(harald)

kongerekke = [haakon, olav, harald]

for konge in kongerekke: konge.skriv()

nåværende_monark = kongerekke[0]
while nåværende_monark is not None:
    nåværende_monark.skriv()
    nåværende_monark = nåværende_monark.etterfølger

