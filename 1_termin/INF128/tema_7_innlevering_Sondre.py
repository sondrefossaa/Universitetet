venner = [['Ole',99887766],['Liv',99778899],['Gro',99556644],
 ['Tom',98675601],['Eva',98987665],['Jan',88997766]]

# oppgave 1 

def finn_venn_index(navn, liste):
    for i, person in enumerate(liste):
        if person[0] == navn:
            return i
    return -1
#a
def finn_telefon(navn : str, liste : list):
    index = finn_venn_index(navn, liste)
    if index != -1:
        print(venner[index][1])
        return
    print("ukjent person")
#finn_telefon("Ole", venner)

#b
def fjern_telefon(navn : str, liste : list):
    index = finn_venn_index(navn, liste)
    if index != -1:
        liste.pop(index)
        return
    print("ukjent person")

#oppgave 2
examen = {'INFO100':'C', 'INFO104':'B', 'INFO116':'E',\
 'INFO180':'A', 'INFO201':'F','INFO280':'C',\
 'GEO101':'D', 'GEO110':'B','ADM101':'A',\
 'ECON100':'B', 'ECON201':'C','GEO210':'C',\
 'FAIL101':'F'}

def karakter_frekvenser(eksamen_dict):
    frekvenser = {}
    for karakter in eksamen_dict.values():
        if karakter in frekvenser:
            frekvenser[karakter] += 1
        else:
            frekvenser[karakter] = 1
    return frekvenser
f = karakter_frekvenser(examen)

def histogram(karakterer_dict : dict):
    karakterer_sortert = sorted(karakterer_dict.keys())
    for karakter in karakterer_sortert:
        print(karakter + " ", end="")
        for i in range(karakterer_dict[karakter]):
            print("*", end="")
        print()
histogram(f)
