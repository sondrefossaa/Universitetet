#!/usr/bin/env python3
"""
Agent LED-system
================
Kjører på Raspberry Pi og blinker LED-signaler basert på simulert tilstand.

Kommentarer merket med [ROS] viser hvordan dette ville vært strukturert
i et ekte ROS-system med noder og topics.
"""

import time
import random
import RPi.GPIO as GPIO

# [ROS] GPIO-pinnen ville vært en ROS-parameter:
#   GPIO_PIN = rospy.get_param("~gpio_pin", 17)
GPIO_PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)


# -----------------------------------------------------------------------
# LED-styring
# -----------------------------------------------------------------------


def led(on: bool):
    GPIO.output(GPIO_PIN, GPIO.HIGH if on else GPIO.LOW)


# -----------------------------------------------------------------------
# Signaler
# -----------------------------------------------------------------------


def solid():
    """Fast lys – system operativt, ingen karakterer sett."""
    print("[signal] Fast lys – klar, ingenting observert")
    led(True)
    time.sleep(3)


def slow_blink():
    """1 Hz puls – én eller flere karakterer i synsfeltet."""
    print("[signal] Langsom puls – karakter(er) detektert")
    for _ in range(4):
        led(True)
        time.sleep(0.5)
        led(False)
        time.sleep(0.5)


def series_blink(n: int, name: str):
    """
    N raske blink × 3 serier – identifiserer én spesifikk karakter.
      1 blink  → Roede    (rød)
      2 blink  → von Bleu (blå)
      3 blink  → Jello    (gul)
      4 blink  → Grønnar  (grønn)
    """
    print(f"[signal] Serieblink ×{n} – {name} identifisert")
    for serie in range(3):
        for _ in range(n):
            led(True)
            time.sleep(0.125)
            led(False)
            time.sleep(0.125)
        if serie < 2:
            time.sleep(1.0)


def no_light():
    """Ingen lys – systemfeil."""
    print("[signal] Ingen lys – SYSTEMFEIL")
    led(False)
    time.sleep(3)


# -----------------------------------------------------------------------
# Karakterer
# [ROS] Disse ville kommet fra /detections publisert av /ball_detector,
#       som bruker HSV-fargefiltrering på bilder fra /camera_node.
# -----------------------------------------------------------------------
CHARACTERS = {
    "Roede": 1,
    "von Bleu": 2,
    "Jello": 3,
    "Grønnar": 4,
}


def get_state() -> dict:
    """
    Returnerer simulert tilstand.

    [ROS] I et ekte system ville /state_estimator abonnert på /detections
          og publisert tilstand på /agent_state. /blink_scheduler ville
          lest /agent_state og sendt kommandoer til /led_command.
    """
    roll = random.random()
    if roll < 0.10:
        return {"status": "fault"}
    elif roll < 0.30:
        return {"status": "operational", "primary": None, "characters": []}
    elif roll < 0.55:
        return {
            "status": "operational",
            "primary": None,
            "characters": list(CHARACTERS.keys()),
        }
    else:
        name = random.choice(list(CHARACTERS.keys()))
        return {"status": "operational", "primary": name, "characters": [name]}


# -----------------------------------------------------------------------
# Hovedløkke
# -----------------------------------------------------------------------

# [ROS] Denne løkken ville vært erstattet av rospy.spin(), og
#       signalene ville blitt trigget av topic-callbacks.

print("Agent LED-system startet. Trykk Ctrl+C for å avslutte.\n")

while True:
    state = get_state()

    # Prioriteringslogikk (høyest → lavest):
    #   1. Systemfeil
    #   2. Spesifikk karakter identifisert
    #   3. Karakter(er) sett
    #   4. Operativt, ingenting observert
    if state["status"] == "fault":
        no_light()

    elif state.get("primary"):
        name = state["primary"]
        series_blink(CHARACTERS[name], name)

    elif state.get("characters"):
        slow_blink()

    else:
        solid()

    print()

