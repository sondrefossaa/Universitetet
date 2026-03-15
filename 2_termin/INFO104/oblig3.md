# Oblig 3

## 1. Førsteordens logikk

---

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

### a

**Situasjonen:**  
Vi har 8 tettsteder: Lillegrend (LIL) på Lilleøy, og Storøyhavn (STOR), Skipperhavn (SKIP), Solvik (SOLV) på Storøy. På fastlandet: Oddeneset (ODD), Dal (DAL), Yttervika (YTT), Berg (BERG).  
To broer er allerede på plass:  

- LIL–ODD  
- STOR–LIL  

Den tredje broen skal gå fra Storøy (altså fra STOR) til et sted på fastlandet.

**Grad av noder før tredje bro:**  

- LIL: forbindelser til ODD og STOR → grad 2  
- STOR: vei til SKIP + bro til LIL → grad 2  
- SKIP: vei til STOR + vei til SOLV → grad 2  
- SOLV: vei til SKIP → grad 1  
- ODD: bro til LIL + vei til DAL → grad 2  
- DAL: vei til ODD + vei til YTT → grad 2  
- YTT: vei til DAL + vei til BERG → grad 2  
- BERG: vei til YTT → grad 1  

To noder har odde grad: SOLV (1) og BERG (1).

---

#### Krav 1: Postbudet – Hamilton-syklus

En Hamilton-syklus krever at **alle noder har grad minst 2**.  
SOLV har bare grad 1, og dette kan ikke endres fordi den tredje broen må gå fra STOR til fastlandet (ikke fra SOLV).  
**Konklusjon:** Umulig å få Hamilton-syklus, uansett hvor tredje bro plasseres.

#### Krav 2: Turistsjefen – Euler-krets

En Euler-krets krever at **alle noder har like grader**.  
Selv om vi velger tredje bro for å forsøke å gjøre SOLV og BERG like, vil STOR sin grad bli odde (fordi STOR får én ekstra forbindelse).  

Eksempel: Bro STOR–BERG gir:  

- STOR: 2 → 3 (odde)  
- BERG: 1 → 2 (jevn)  
- SOLV: 1 (fremdeles odde)  

Da har vi to odde noder (STOR og SOLV) – mulig med Euler-sti, men ikke krets. For å få krets må alle være like, men det er umulig med bare én ny bro til fastlandet.  
**Konklusjon:** Euler-krets umulig.

---

**Svar på spørsmålene:**  
(i) **Finnes løsning som oppfyller begges krav samtidig?**  
Nei – Hamilton-syklus er umulig uansett.

(ii) **Finnes løsning som oppfyller kravene hver for seg?**  
Nei – Hamilton-syklus er umulig (pga. SOLVs grad 1). Euler-krets er umulig (kan ikke få alle like).

---

### b

**Graf (i):**  

- Kun to broer: LIL–ODD og STOR–LIL  
- Ingen bro mellom Storøy og fastlandet utover disse  
- Opprinnelige veier:  
  - Storøy: STOR–SKIP–SOLV  
  - Fastland: ODD–DAL–YTT–BERG  
  - Antatt: ingen vei YTT–STOR  

Gradfølge (i):  
LIL(2), STOR(2), SKIP(2), SOLV(1), ODD(2), DAL(2), YTT(2), BERG(1)  
→ To noder med grad 1: SOLV og BERG.

**Graf (ii):**  

- Samme to faste broer  
- Ny bro mellom BERG og SOLV  
- Veien YTT–STORHAVN fjernet (men denne fantes ikke i (i), så ingen endring her)  

Det vil si: (ii) = (i) + kant BERG–SOLV.  

Da blir nye grader:  
SOLV: 1 → 2  
BERG: 1 → 2  
Resten uendret.  

Gradfølge (ii): LIL(2), STOR(2), SKIP(2), SOLV(2), ODD(2), DAL(2), YTT(2), BERG(2)  
→ Alle noder har grad 2.

**Sammenligning:**  

- (i) har to noder med grad 1  
- (ii) har ingen noder med grad 1  

Ulike gradsekvenser → **ikke isomorfe**.

---

**Svar (b):**  
Nei, grafene er ikke isomorfe fordi gradsekvensene er forskjellige.

# Oppgave 3 Kombinatorikk

## Oppgave a

bokstaver + tall = 26 + 10 = 36
10 * 26 * (6 * 36) = 56160
## Oppgave b
#### a) 
hver n har n mulige verdier
n¨n
#### b)
Blir en permutasjon av mengen av n elementer, altså
n!
#### c)
n opphøyd i ceil(m/2)
