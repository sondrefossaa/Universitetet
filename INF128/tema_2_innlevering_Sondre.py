import math as m
import random as r
#Oppgave 1
print((3+2)*8/(4-3))

#Oppgave 2
fornavn = input("fornavn: ")
etternavn = input("Etternavn: ")

print(f"Det er {len((fornavn+etternavn))} bokstaver i navnet ditt")

#Oppgave 3
passasjerer = int(input("Hvor mange passasjerer skal du hente? "))
bil_plass = int(input("Hvor mange passasjerer har du plass til i bilen? "))
print(f"Du må kjøre {m.ceil(passasjerer/bil_plass)} turer for å hente alle sammen.")

#Oppgave 4
tall = input("Gi meg et tall: ")
tall2 = tall + str(r.randint(0, 9))
print(f"{tall2}/{tall} = {int(tall2)/int(tall)}")