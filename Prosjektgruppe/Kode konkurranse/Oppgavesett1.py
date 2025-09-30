""" Torbjørn har ganske mange venner, men de er av varierende kvalitet. Noen er ekte, noen er falske, noen er snille, noen er slemme, noen har lite penger, noen har mye penger, noen har bil, noen har sykkel, noen har månedskort på bybanen, han ene har en skikkelig kul stekepanne i rustfritt stål og en av dem har en bestefar som drepte nazister under andre verdenskrig. Dette er mye informasjon for Torbjørn å bære rundt på, så han har laget et system hvor han gir hver venn en score fra 1 - 10. Lag et program som går gjennom listen til Torbjørn og finner ut hvor mange dårlige venner han har, vi kan anta at dårlige venner har en score under 5.

Her er listen over Torbjørns venner:
venner = [8, 7, 6, 9, 8, 5, 4, 5, 6, 3, 7, 8, 9, 6, 7, 1, 2, 7, 5, 4, 7, 8, 5, 6, 7, 5, 3]

Eksempel output: ‘Torbjørn har 6 dårlige venner’ """
venner = [8, 7, 6, 9, 8, 5, 4, 5, 6, 3, 7, 8, 9, 6, 7, 1, 2, 7, 5, 4, 7, 8, 5, 6, 7, 5, 3]
dårlig = 0

for venn in venner:
    if venn < 5:
        dårlig += 1

print(f"Torbjørn har {dårlig} dårlige venner.")