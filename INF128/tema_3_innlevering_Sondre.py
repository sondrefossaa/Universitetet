#Oppg.1
#A
# x!=7 blir true og y<=50 blir false
#X>7 or x<7

#Oppg. 2
def oppgave_2():
    alder = int(input("Oppgi alder: "))
    by_år= int(input("Hvor lenge had du bodd i tulleby? "))

    text = ""
    fra_ordfører = 0
    ordfører_kval ={
        "alder": 30,
        "by": 9
    }
    bystyre_kval={
        "alder":25,
        "by":5
    }
    fra_ordførerA = ordfører_kval["alder"] - alder
    fra_ordførerB = ordfører_kval["by"] - by_år
    fra_bystyreA = bystyre_kval["alder"] - alder
    fra_bystyreB = bystyre_kval["by"] - by_år

    text = ""

    bystyre = True if (fra_bystyreA <= 0 and fra_bystyreB <= 0) else False

    ordfører = True if (fra_ordførerA <= 0 and fra_ordførerB <= 0) else False

    if ordfører:
        print("Du kan bli ordfører og sitte i bystyret")
    elif bystyre:
        print(f"Du kan sitte i bystyret")
        print(f"Prøv igjen om {max(fra_ordførerB, fra_ordførerA)} år for å bli ordfører")
    else:
        print(f"Du er ikke kvalifisert enda, prøv igjen om {max(fra_bystyreA, fra_bystyreB)} år")

#Oppgave 3
def oppgave_3():
    x = int(input('tall: '))
    if x <= 5:
        print('max 5')
    elif x < 10:
        print('6,7,8 eller 9')
    else:
        print('minst 10')

oppgave_2()
oppgave_3()
