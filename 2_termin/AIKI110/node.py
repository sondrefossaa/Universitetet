"""
led_controller.py
=================
Simulerer LED-kommunikasjon for agentsystemet beskrevet i «Agentsystemets arkitektur».

Når dette programmet omsider kjøres som en ROS-node (/blink_scheduler + /led_controller),
vil det lytte på følgende topics:

    /agent_state  (std_msgs/String eller custom AgentState.msg)
        Forventet innhold:
          - hvilke karakterer som er synlige: ["roede", "von_bleu", "jello", "groennar"]
          - posisjon per karakter: {"x": float, "y": float}  (normalisert -1.0 til 1.0)
          - avstand per karakter: "near" | "mid" | "far"
          - antall karakterer synlige: int
          - systemstatus: "ok" | "camera_error" | "node_down"

    /detections  (publisert av /ball_detector)
        Forventet innhold:
          - liste med detekterte baller med farge, posisjon og størrelse

    /system_health  (publisert av en watchdog-node)
        Forventet innhold:
          - status for hver node: "ok" | "error"

Programmet bruker GPIO (RPi.GPIO) for å styre en fysisk LED på en Raspberry Pi.
I simuleringsmodus (SIMULATE = True) printes blink-mønstrene til terminalen i stedet.

LED-signaler (ref. dokumentet, Del 3):
  - Fast lys            : Operativt, ingen karakterer sett
  - Langsom puls 1 Hz   : Én eller flere karakterer detektert
  - Serie-blink 1–4     : Hvilken spesifikk karakter (1=Roede, 2=vonBleu, 3=Jello, 4=Groennar)
  - Posisjonsblink      : Antall blink i rask serie indikerer posisjon (se CHARACTER_POSITION)
  - Avstandssignal      : Blinkfrekvens indikerer avstand (nær=rask, fjern=langsom)
  - Uregelmessig flikk  : Systemfeil – krever menneskelig inngripen
"""

import time
import random

# ── Konfigurasjon ──────────────────────────────────────────────────────────────
SIMULATE = True  # Sett False på Raspberry Pi med fysisk LED
LED_PIN = 17  # GPIO-pin (BCM-nummerering) for LED

if not SIMULATE:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

# ── Karakterer og koder ────────────────────────────────────────────────────────
CHARACTERS = {
    "roede": {"id": 1, "color": "rød", "description": "Roede"},
    "von_bleu": {"id": 2, "color": "blå", "description": "von Bleu"},
    "jello": {"id": 3, "color": "gul", "description": "Jello"},
    "groennar": {"id": 4, "color": "grønn", "description": "Grønnar"},
}


# Posisjon: x-akse normalisert -1.0 (helt venstre) til 1.0 (helt høyre)
# Kodes som antall ekstra blink etter karakter-ID-blink:
#   1 blink = venstre, 2 blink = midten, 3 blink = høyre
def position_code(x: float) -> tuple[int, str]:
    if x < -0.33:
        return 1, "venstre"
    elif x > 0.33:
        return 3, "høyre"
    else:
        return 2, "midten"


# Avstand: størrelse på deteksjonsrektangel → "near", "mid", "far"
DISTANCE_HZ = {
    "near": 5.0,  # rask blinking = nær
    "mid": 2.0,
    "far": 0.8,  # langsom blinking = langt unna
}


# ── Primitiver: LED på/av ──────────────────────────────────────────────────────
def led_on():
    if SIMULATE:
        print("  💡 ON ", end="", flush=True)
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)


def led_off():
    if SIMULATE:
        print("OFF", flush=True)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


def blink_once(on_time=0.1, off_time=0.1):
    led_on()
    time.sleep(on_time)
    led_off()
    time.sleep(off_time)


# ── Signal A: Fast lys – operativt, ingen karakterer ──────────────────────────
def signal_steady(duration=3.0):
    """
    Fast, konstant lys i `duration` sekunder.
    Mening: Systemet er operativt. Ingen karakterer observert akkurat nå.
    """
    print("\n[SIGNAL] Fast lys → Operativt, ingen karakterer sett")
    led_on()
    time.sleep(duration)
    led_off()


# ── Signal B: Langsom puls – karakter(er) detektert ───────────────────────────
def signal_slow_pulse(duration=3.0):
    """
    Jevn puls 1 Hz (0.5 s på, 0.5 s av).
    Mening: Én eller flere karakterer er synlige i kameraets synsfelt.
    """
    print("\n[SIGNAL] Langsom puls → Karakter(er) detektert")
    end = time.time() + duration
    while time.time() < end:
        blink_once(on_time=0.5, off_time=0.5)


# ── Signal C: Serie-blink – hvem er det? + posisjon ───────────────────────────
def signal_character_id(char_key: str, x_pos: float = 0.0, repeats=3):
    """
    Identifiserer en spesifikk karakter og dens horisontale posisjon.

    Format per serie:
      [N raske blink]  PAUSE  [P posisjonsblink]
      N = karakter-ID (1=Roede, 2=vonBleu, 3=Jello, 4=Groennar)
      P = posisjon    (1=venstre, 2=midten, 3=høyre)

    Serien gjentas `repeats` ganger med 1 sek pause mellom.
    """
    char = CHARACTERS[char_key]
    n = char["id"]
    p_count, p_label = position_code(x_pos)

    print(f"\n[SIGNAL] Karakter-ID → {char['description']} ({char['color']} ball)")
    print(f"         Posisjon   → {p_label}  (x={x_pos:+.2f})")
    print(f"         Mønster    → {n} blink | pause | {p_count} blink  (×{repeats})")

    for r in range(repeats):
        print(f"  Serie {r + 1}/{repeats}:", end=" ")
        # Karakter-ID blink
        for _ in range(n):
            blink_once(on_time=0.15, off_time=0.15)
        time.sleep(0.5)  # pause mellom ID og posisjon
        # Posisjonsblink
        for _ in range(p_count):
            blink_once(on_time=0.25, off_time=0.2)
        print()
        if r < repeats - 1:
            time.sleep(1.0)  # pause mellom serier


# ── Signal D: Avstandssignal – hvor langt unna er karakteren? ─────────────────
def signal_distance(distance: str, duration=3.0):
    """
    Blinkfrekvens kommuniserer avstand til nærmeste detekterte karakter.
      near → 5 Hz  (veldig raskt)
      mid  → 2 Hz
      far  → 0.8 Hz (langsomt)

    Mening: Gir mennesket en indikasjon på om roboten er i nærheten av karakteren.
    """
    hz = DISTANCE_HZ.get(distance, 2.0)
    period = 1.0 / hz
    on_t = period * 0.4
    off_t = period * 0.6

    print(f"\n[SIGNAL] Avstand → '{distance}'  ({hz} Hz)")
    end = time.time() + duration
    while time.time() < end:
        blink_once(on_time=on_t, off_time=off_t)


# ── Signal E: Systemfeil ───────────────────────────────────────────────────────
def signal_system_error(duration=4.0):
    """
    Uregelmessig flakking – skiller seg visuelt fra alle planlagte mønstre.
    Mening: Kritisk node eller kamera svarer ikke. Krever menneskelig inngripen.
    """
    print("\n[SIGNAL] ⚠️  SYSTEMFEIL – uregelmessig flakking")
    end = time.time() + duration
    while time.time() < end:
        on_t = random.uniform(0.04, 0.18)
        off_t = random.uniform(0.04, 0.35)
        blink_once(on_time=on_t, off_time=off_t)


# ── Tilstandsmaskin – velger signal basert på agent_state ─────────────────────
def run_state(state: dict):
    """
    Tar inn en tilstandsbeskrivelse (tilsvarer det som ville komme fra /agent_state)
    og spiller av riktig LED-sekvens.

    Eksempel på state-dict (erstatter ROS-melding):
    {
        "system_status": "ok",          # "ok" | "camera_error" | "node_down"
        "detections": [
            {"char": "roede",   "x": -0.5, "distance": "near"},
            {"char": "jello",   "x":  0.1, "distance": "far"},
        ]
    }

    Prioritet (høy → lav):
      1. Systemfeil
      2. Karakter-ID + posisjon  (første deteksjon i listen)
      3. Avstand til nærmeste karakter
      4. Langsom puls (noe er sett, men ingen ID valgt)
      5. Fast lys (ingenting sett)
    """
    if state.get("system_status") != "ok":
        signal_system_error()
        return

    detections = state.get("detections", [])

    if not detections:
        signal_steady()
        return

    # Karakter-ID + posisjon for første (viktigste) deteksjon
    first = detections[0]
    signal_character_id(first["char"], x_pos=first.get("x", 0.0))
    time.sleep(0.5)

    # Avstand til samme karakter
    signal_distance(first.get("distance", "mid"))

    # Hvis det er flere karakterer – langsom puls som indikasjon
    if len(detections) > 1:
        print(f"\n  (+ {len(detections) - 1} andre karakter(er) i synsfeltet)")
        signal_slow_pulse(duration=2.0)


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  LED-KONTROLLER – Agentsystem demo")
    print("  (SIMULATE =", SIMULATE, ")")
    print("=" * 60)

    scenarios = [
        {
            "label": "Scenario 1: Operativt, ingenting sett",
            "state": {"system_status": "ok", "detections": []},
        },
        {
            "label": "Scenario 2: Roede er nær til venstre",
            "state": {
                "system_status": "ok",
                "detections": [{"char": "roede", "x": -0.7, "distance": "near"}],
            },
        },
        {
            "label": "Scenario 3: von Bleu er langt unna, midten",
            "state": {
                "system_status": "ok",
                "detections": [{"char": "von_bleu", "x": 0.05, "distance": "far"}],
            },
        },
        {
            "label": "Scenario 4: Jello nær høyre + Grønnar i synsfeltet",
            "state": {
                "system_status": "ok",
                "detections": [
                    {"char": "jello", "x": 0.8, "distance": "near"},
                    {"char": "groennar", "x": -0.2, "distance": "mid"},
                ],
            },
        },
        {
            "label": "Scenario 5: Grønnar på midten, middels avstand",
            "state": {
                "system_status": "ok",
                "detections": [{"char": "groennar", "x": 0.1, "distance": "mid"}],
            },
        },
        {
            "label": "Scenario 6: SYSTEMFEIL – kamera svarer ikke",
            "state": {"system_status": "camera_error", "detections": []},
        },
    ]

    for s in scenarios:
        print("\n" + "─" * 60)
        print(f"  {s['label']}")
        print("─" * 60)
        run_state(s["state"])
        time.sleep(1.0)

    print("\n" + "=" * 60)
    print("  Demo ferdig.")
    print("=" * 60)

    if not SIMULATE:
        GPIO.cleanup()
