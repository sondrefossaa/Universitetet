#Oppgave b

input = "Lennart hater lange ord"
ordFraInput = input.split()

lengde = []
for ord in ordFraInput:
    lengde.append(len(ord))
print(lengde)