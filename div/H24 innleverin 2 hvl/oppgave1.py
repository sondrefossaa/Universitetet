tall = 1
tall_liste = []
while tall != 0:
    tall = int(input("Skriv inn et positivt tall (eller 0 når du er ferdig):\n"))
    tall_liste.append(tall)

deletall = int(input("Hvilket tall vil du dele tallene over på?\n"))
# Finn tall som er  delelige på to og ikke delelige på to
delelig =  []
ikke_delelig = []

for temp_tall in tall_liste:
    if temp_tall % deletall == 0:
        delelig.append(temp_tall)
    else:
        ikke_delelig.append(temp_tall)
print(f"Delelig på {deletall}:\n")
print(delelig)

print(f"Ikke delelig på {deletall}:\n")
print(ikke_delelig)