text = """Jeg traff henne på St. Hanshaugen sommer'n 89
Hun gråt når hun var full og sang når hun var blid
Jeg elsket henne høyt, hun elsket meg vilt
Høsten kom, døra smalt og etterpå ble det stilt
Så jeg traff ei lita jente en regnfull vår
Med bløte konsonanter og regnvått hår
Hun lovet meg troskap, jeg lovet henne alt
Vinter'n kom, troskap gikk og etterpå ble det kaldt
Jenter som kommer og jenter som går
Jenter som glipper, jenter du aldri får
Jenter som smiler en tidlig vår
Jenter og en litt sliten matador
Hey, hey
Hey, hey
Hey, hey, hey
Ved Frognerparken møtes to trikker kvart på ni
Og hun smilte bak ruten til vinter'n var forbi
Jeg skrev I rutens morgendugg "Jeg tror jeg elsker deg"
Men våren kom og isen gikk og hun seilte sin vei
Jenter som kommer og jenter som går
Jenter som glipper, jenter du aldri får
Jenter som smiler en tidlig vår
Jenter og en litt sliten matador
Hey, hey
Hey, hey
Hey, hey, hey
Hey, hey, hey, hey
EY
Månen er gul og titter ned på skrå
Gud er en fyr det kan være vanskelig å forstå
Jeg kikker meg I speilet, årene går
Hei, jeg heter Berger, jeg er matador
Jenter som kommer og jenter som går
Jenter som glipper, jenter du aldri får
Jenter som smiler en tidlig vår
Jenter og en litt sliten matador
Hey, hey!
Jenter som kommer og jenter som går
Jenter som glipper, jenter du aldri får
Jenter som smiler en tidlig vår
Jenter og en litt sliten matador
Hey, hey
"""
i = 0
ordArray = []
ord_Lib = {}
ord = ""
for i in range(len(text)):
    if text[i].isalpha():
        ord += text[i]
    elif ord != '':
        ord = ord.lower()
        if ord in ord_Lib:
            ord_Lib[ord] += 1
        else:
            ord_Lib[ord] = 1
        ord = ""
max_value = 0
max_ord = ""
for ord in ord_Lib:
    if ord_Lib[ord] > max_value:
        max_value = ord_Lib[ord]
        max_ord = ord
max_ord_kort = max(ord_Lib, key=ord_Lib.get)
print(ord_Lib)
print(f"Ordet {max_ord_kort} brukes {max_value} ganger.")
    #if ord_Lib[i].value > max_value:
        

