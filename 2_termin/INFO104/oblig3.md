# Oblig 3 - Sondre Fosså

## 1. Førsteordens logikk

### A

- **Konstanter**: Ingen
- **Predikatsymboler**:
  - Student(x) aritet 1,
  - Glad(x) aritet 1
  - Irritert(x) aritet 1
- Formel:
  Eks x Student(x) & Glad(x) & Irritert(x)

### B

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Flink(·) aritet 1
  - Sykepleier(·) aritet 1
  - Rik(·) aritet 1
- **Formel:**
    ∀x ((Flink(x) ∧ Sykepleier(x)) → ¬Rik(x))

### C

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Dum(·) aritet 1
  - Lærer(·) aritet 1
  - Høy(·) aritet 1
- **Formel:**
    ∀x ((Dum(x) ∧ Lærer(x)) → ¬Høy(x))

### D

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Bil(·) aritet 1
  - Fin(·) aritet 1
  - Gammel(·) aritet 1
- **Formel:**
    ∃x (Bil(x) ∧ ¬Fin(x) ∧ ¬Gammel(x))

### E

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Kjedelig(·) aritet 1
  - Uærlig(·) aritet 1
- **Formel:**
    ¬∀x Kjedelig(x) ∨ ¬∃x Uærlig(x)

### F

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Dommer(·) aritet 1
  - Høy(·) aritet 1
  - Berømt(·) aritet 1
- **Formel:**
    (∀x (Dommer(x) → Høy(x))) → ∃x (Dommer(x) ∧ Berømt(x))

### G

- **Konstanter:**
  - a (Anne) (konstant, aritet 0)
- **Predikatsymboler:**
  - Journalist(·) aritet 1
  - Redaktør(·) aritet 1
  - Kjenner(·,·) aritet 2
- **Formel:**
    Journalist(a) → ¬∃x (Redaktør(x) ∧ Kjenner(x, a))

### H

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Kjenner(·,·) aritet 2
  - Lav(·) aritet 1
  - Republikaner(·) aritet 1
- **Formel:**
    ¬∃x ∃y (Kjenner(x, y) ∧ Lav(y) ∧ Republikaner(y))

### I

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Kjedelig(·) aritet 1
  - Professor(·) aritet 1
  - Høy(·) aritet 1
- **Formel:**
    ∀x ((Kjedelig(x) ∧ Professor(x)) → Høy(x))

### J

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Sårer(·,·) aritet 2
- **Formel:**
    ∃x ∀y Sårer(x, y)

### K

- **Konstanter:**
  - a (Anne)
- **Predikatsymboler:**
  - Kjenner(·,·) aritet 2
- **Formel:**
    ∀x Kjenner(a, x)

### L

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Forstår(·,·) aritet 2
- **Formel:**
    ∃x ∀y Forstår(y, x)

### M

- **Konstanter:** Ingen
- **Predikatsymboler:**
  - Student(·) aritet 1
  - Liker(·,·) aritet 2
  - Gretten(·) aritet 1
- **Formel:**
    ¬∃x (¬Student(x) ∧ ∀y (Gretten(y) → Liker(x, y)))

## 2 Grafer

## a

Postbudet vil ha en hamilton syklus og Turistskjefen vil ha en eulercyclus

**Postbudet**
Kravet til Postbudet kan oppfylles av å ha en bro mellom berg og solvik

**Turistskjefen**
En eulercyclus er valid når alle noder har partall antall kanter eller bare start
og slutt noden har odde kanter.
Dersom vi skal starte å slutte i samme node må alle nodene i grafen ha
partall kanter og det har ikke lillegrend noden.
Derfor kan ikke kravet til Turistskjefen oppfylles.

### Svar på i og ii

Det finnes bare en løsning som oppfyller kravet til Postbudet.

### b

**Graf (i):**  

Gradfølge (i):  
LIL(2), STOR(2), SKIP(2), SOLV(1), ODD(2), DAL(2), YTT(2), BERG(1)  
To noder med grad 1: SOLV og BERG.

**Graf (ii):**  

- Ny bro mellom BERG og SOLV

Det vil si: (ii) = (i) + kant BERG–SOLV.  

Da blir nye grader:  
SOLV: 1 → 2  
BERG: 1 → 2  
Resten uendret.  

Gradfølge (ii): LIL(2), STOR(2), SKIP(2), SOLV(2), ODD(2), DAL(2), YTT(2), BERG(2)  
Alle noder har grad 2.

i og ii har ulike gradsekvenser og er derfor ikke isomorfe

## Oppgave 3 Kombinatorikk

### Oppgave a

bokstaver + tall = 26 + 10 = 36
Svaret blir: 10 &times; 26 &times; (pow(36, 6))

### Oppgave b

#### a)

hver n har n mulige verdier
pow(n, 2)

#### b)

Blir en permutasjon av mengen av n elementer, altså
n!

#### c)

n opphøyd i ceil(m/2)
