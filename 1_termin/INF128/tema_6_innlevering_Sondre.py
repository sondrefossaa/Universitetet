#1
def oppgave_1():
    print("Legg til navn og nummer, avslutt med <enter>")

    with open("telefon.txt", "a", encoding="utf-8") as file:
        while (ny_person := input("Navn og nummer: ")) != "":
            file.write(ny_person + "\n")

#2
def oppgave_2():

    with open("telefon.txt", "r", encoding="utf-8") as file:
        navn = input("Navn: ")
        gammelt_nummer = input("Gammelt telefonnummer: ")
        nytt_nummer = input("Nytt nummer: ")
        linjer = file.readlines()
        
        for i in range(len(linjer)):
            if linjer[i] == navn + " " + gammelt_nummer + "\n":
                linjer[i] = navn + " " + nytt_nummer + "\n"

    with open("telefon.txt", "w", encoding="utf-8") as file:
        file.writelines(linjer)

#3

def fjern_vokaler_egen():
    vokaler = "aeiouyæøåAEIOUYÆØÅ"

    with open("test_text.txt", "r", encoding="utf-8") as file:
        linjer = file.readlines()
        
        for i in range(len(linjer)):
            for vokal in vokaler:
                linjer[i] = linjer[i].replace(vokal, "")
            

    with open("test_text.txt", "w", encoding="utf-8") as file:
        file.writelines(linjer)

# Mer optimalt (hjelp av deepseek)
def fjern_vokaler(filvei : str):
    vokaler = "aeiouyæøåAEIOUYÆØÅ"
    oversettelse_tabell = str.maketrans("", "", vokaler)
    print("Legg til navn og nummer, avslutt med <enter>")

    with open(filvei, "r", encoding="utf-8") as file:
        #linjer = file.readlines()
        linjer = [linje.translate(oversettelse_tabell) for linje in file]

    with open("ny" + filvei, "w", encoding="utf-8") as file:
        file.writelines(linjer)
fjern_vokaler("test_text.txt")