# Oblig 4

## oppgave 1

- Ramada Inn = R, P(R) = 0.2
- Sheraton = S, P(S) = 0.5
- Lakeview Motor Lodge = L, P(L) = 0.3
- F = faulty plumbing
- P(F∣R)=0.05,P(F∣S)=0.04,P(F∣L)=0.08

### A, 1.84)
#### a)

Bruk total sannsylighet:
P(F)=P(R)P(F∣R)+P(S)P(F∣S)+P(L)P(F∣L)
P(F)=(0.2)(0.05)+(0.5)(0.04)+(0.3)(0.08)
P(F)=0.01+0.02+0.024=0.054 = 5.4%

#### b)

Bayes teorem:
Faulty fra Lakeview delt på totalt faulty gir oss sannsyligheten for at
et faulty rom kommer fra Lakeview
P(L|F) = (P(L)·P(F|L)) / P(F)

P(L|F) = (0.3·0.08) / 0.054

P(L|F) = 0.024 / 0.054 ≈ 0.444 = 44%

### B, 1.91)
Bayes theorem 
D: Damen har kreft
nD: Damen har ikke kreft
N: Reslultatet er negativt
Vi vil ha diagnose gitt negativt resultat som er : P(D|N)
P(D|N)= P(D)P(N|D) / P(D)P(N|D)+P(¬D)P(N∣¬D)P(D)P(N|D)
= 0.007 / 0.8905 ≈ 79%


### C, 1.93)
Gitt:
- P(E1) = 0.7, P(E2) = 0.3
- P(A | E1) = 0.02
- P(A | E2) = 0.04

## 1. Finn P(A)

P(A) = 0.7 * 0.02 + 0.3 * 0.04  
P(A) = 0.014 + 0.012 = 0.026

## 2. Bayes

P(E1 | A) = 0.014 / 0.026 ≈ 0.54  

P(E2 | A) = 0.012 / 0.026 ≈ 0.46  

## 3. Svar

Ingeniør 1 er mest sannsynlig (ca. 54%)



# Oppgave 2: Kombinatorikk, sannsynlighet, informasjonsteori

Vi antar at det finnes 25 ulike emojier.

---

## a) Hvor mange ulike sekvenser av minst 2 og opp til 5 emojier finnes?

For en sekvens med lengde n finnes det:

25^n

muligheter, siden hver plass kan fylles med en av 25 emojier.

Vi skal ha lengde 2, 3, 4 eller 5:

25^2 + 25^3 + 25^4 + 25^5

= 625 + 15625 + 390625 + 9765625

= 10172500

**Svar:** 10172500

---

## b) Hvor mange ulike sekvenser av 5 emojier starter med 🤠?

Første emoji er fast: 🤠

Da er det 4 plasser igjen, og hver av dem kan fylles på 25 måter:

25^4 = 390625

**Svar:** 390625

---

## c) Hvor mange ulike sekvenser av 5 emojier inneholder 😂 eller 🤠 eller begge deler?

Totalt antall sekvenser av lengde 5 er:

25^5

Antall sekvenser som ikke inneholder verken 😂 eller 🤠:

23^5

Så antall som inneholder minst én av dem er:

25^5 - 23^5

= 9765625 - 6436343

= 3329282

**Svar:** 3329282

---

## d) Hvor mange ulike sekvenser med 5 ulike emojier finnes?

Her skal alle 5 være forskjellige.

Da får vi:

25 * 24 * 23 * 22 * 21

= 6375600

**Svar:** 6375600

---

## e) Hva er sannsynligheten for at en tilfeldig sekvens av 4 ulike emojier inneholder 🤠, 😂, 👁 og 👄?

Totalt antall sekvenser av 4 ulike emojier er:

25 * 24 * 23 * 22

For at sekvensen skal inneholde akkurat 🤠, 😂, 👁 og 👄, må den bestå av disse 4 emojiene i en eller annen rekkefølge.

Antall gunstige sekvenser er derfor:

4! = 24

Sannsynligheten blir:

24 / (25 * 24 * 23 * 22)

= 1 / (25 * 23 * 22)

= 1 / 12650

≈ 0.0000791

**Svar:** 1 / 12650 ≈ 0.0000791

---

## f) Hva er sannsynligheten for at en tilfeldig sekvens av 4 ulike emojier inneholder 🤠, 😂 og 👁?

Totalt antall sekvenser av 4 ulike emojier er:

25 * 24 * 23 * 22

Sekvensen må inneholde 🤠, 😂 og 👁, pluss én ekstra emoji valgt blant de resterende 22.

- Velg den fjerde emojien: 22 måter
- Ordne de 4 emojiene: 4! = 24 måter

Antall gunstige sekvenser:

22 * 24

Sannsynligheten blir:

(22 * 24) / (25 * 24 * 23 * 22)

= 1 / (25 * 23)

= 1 / 575

≈ 0.001739

**Svar:** 1 / 575 ≈ 0.001739

---

## g) Millennials bruker 😂 i 9 av 10 meldinger, mens ikke-millennials bruker den i 1 av 20 meldinger. 10% av kontaktene er millennials. Hva er sannsynligheten for at en melding som inneholder 😂 er fra en millennial?

La:

- M = meldingen er fra en millennial
- I = meldingen inneholder 😂

Gitt:

- P(M) = 0.1
- P(ikke M) = 0.9
- P(I | M) = 0.9
- P(I | ikke M) = 0.05

Først finner vi P(I):

P(I) = 0.9 * 0.1 + 0.05 * 0.9

= 0.09 + 0.045

= 0.135

Så bruker vi Bayes:

P(M | I) = (0.9 * 0.1) / 0.135

= 0.09 / 0.135

= 2 / 3

≈ 0.667

**Svar:** 2 / 3 ≈ 0.667

---

## h) Hvor mye informasjon, målt i bits, bærer en sekvens av 4 emojier dersom alle sekvenser er like sannsynlige?

Antall mulige sekvenser av 4 emojier er:

25^4 = 390625

Når alle er like sannsynlige, er informasjonsmengden:

log2(390625)

= log2(25^4)

= 4 * log2(25)

≈ 4 * 4.643856

≈ 18.58

**Svar:** ca. 18.58 bits

---

## i) Hvor mye informasjon bærer nå en sekvens av 4 emojier, gitt at du vet at den er sendt av en millennial?

Vi vet:

- Millennials bruker 😂 i 9 av 10 meldinger
- Alle sekvenser med 😂 er like sannsynlige
- Alle sekvenser uten 😂 er like sannsynlige

Totalt antall sekvenser av 4 emojier:

25^4 = 390625

Antall sekvenser uten 😂:

24^4 = 331776

Antall sekvenser med minst én 😂:

390625 - 331776 = 58849

Da blir sannsynligheten til én bestemt sekvens:

- Hvis den inneholder 😂:
  0.9 / 58849

- Hvis den ikke inneholder 😂:
  0.1 / 331776

Informasjonsinnholdet i en sekvens er:

I(x) = -log2(P(x))

### Sekvens med 😂

I = -log2(0.9 / 58849)

≈ 15.997 bits

### Sekvens uten 😂

I = -log2(0.1 / 331776)

≈ 21.662 bits

Siden oppgaven spør hvor mye informasjon en sekvens bærer gitt at den er sendt av en millennial, er det mest naturlig å oppgi gjennomsnittet:

H = 0.9 * 15.997 + 0.1 * 21.662

≈ 16.56 bits

**Svar:** ca. 16.56 bits i gjennomsnitt

---

## j) Kort intuitiv forklaring på forskjellen mellom h) og i)

I h) antok vi at alle sekvenser av 4 emojier var like sannsynlige. Da er usikkerheten størst, og informasjonsmengden blir høy.

I i) vet vi mer på forhånd: meldingen kommer fra en millennial, og millennials bruker ofte 😂. Da blir noen sekvenser mer sannsynlige enn andre. Når noe er mer forutsigbart, gir det mindre ny informasjon.

Derfor er svaret i i) lavere enn i h).
