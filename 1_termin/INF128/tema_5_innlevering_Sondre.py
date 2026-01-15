# Oppgave 1
def antallVokaler(text : str):
    vokaler = ['a', 'e', 'i', 'o', 'u', 'y', 'æ', 'ø', 'å']
    return len([a for a in text if a in vokaler])

print(antallVokaler('Tre små musikanter på Høybro plass'))




# Oppgave 2

TV= \
'''
Tulleveien Velforening
leder: Kari
kasserer: Ole
IT-ansvarlig: Liv
parkeringsansvarlig: Kari
arrangementsansvarlig: Liv
hagekonsulent: Kari
brannansva
'''
def verv(navn : str, liste : str = TV):
    verv = []
    for i in range(len(liste)):
        if liste[i:i+len(navn)] == navn:
            j = -2
            while liste[i+j] != '\n':
                j -= 1
            verv.append(liste[i+j+1:i-2])
    return verv

print(verv("Kari"))
    