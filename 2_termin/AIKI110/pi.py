import RPi.GPIO as GPIO
import time
import sys
import signal

# lobal variabel for prikk-varighet (i sekunder)
PRIKK_VARIGHET = 0.2

# Morse-kode mapping (fra oppgaven)
MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "Æ": ".-.-",
    "Ø": "---.",
    "Å": ".--.-",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    " ": " ",  # Mellomrom mellom ord
}

# GPIO-pinne (bruk BCM-nummerering)
LED_PIN = 14  # Endre denne til din tilkobling


class MorseBlinker:
    def __init__(self, pin, numbering_mode=GPIO.BCM):
        """
        Initialiserer GPIO og oppsett
        """
        # Velg nummereringsformat
        if numbering_mode == GPIO.BCM:
            GPIO.setmode(GPIO.BCM)
            print("Bruker BCM-nummerering")
        else:
            GPIO.setmode(GPIO.BOARD)
            print("Bruker fysisk pin-nummerering")

        # Sett opp pin som output
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

        # For å håndtere Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

        print(f"GPIO {pin} satt opp som output")

    def signal_handler(self, sig, frame):
        """
        Håndterer Ctrl+C for å frigjøre ressurser
        """
        print("\nAvbryter program...")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        """
        Frigjør GPIO-ressurser
        """
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup()
        print("GPIO-ressurser frigjort")

    # Oppgave 1: Enkel blinking
    def blink_one_second(self):
        """
        Blinker LED i ett sekund
        """
        print("Blinker i 1 sekund...")
        GPIO.output(self.pin, GPIO.HIGH)  # Lys på
        time.sleep(1)  # Vent 1 sekund
        GPIO.output(self.pin, GPIO.LOW)  # Lys av
        print("Ferdig")

    # Oppgave 2: Kort blink
    def short_blink(self, duration=0.2):
        """
        Gir et kort blink med gitt varighet
        """
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.pin, GPIO.LOW)

    def blink_twice(self):
        """
        Blinker to ganger (kort blink)
        """
        print("Blinker to ganger...")
        for i in range(2):
            self.short_blink()
            if i < 1:  # Vent mellom blink, men ikke etter siste
                time.sleep(PRIKK_VARIGHET)

    # Oppgave 3: Blink en bokstav i morse
    def blink_morse_char(self, char):
        """
        Blinker en enkelt bokstav i morse
        """
        char = char.upper()
        if char not in MORSE:
            print(f"Ugyldig tegn: {char}")
            return

        morse_code = MORSE[char]
        print(f"Blinker {char}: {morse_code}")

        for symbol in morse_code:
            if symbol == ".":
                # Prikk - kort signal
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(PRIKK_VARIGHET)
                GPIO.output(self.pin, GPIO.LOW)
            elif symbol == "-":
                # Strek - tre ganger prikk
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(3 * PRIKK_VARIGHET)
                GPIO.output(self.pin, GPIO.LOW)
            elif symbol == " ":
                # Mellomrom mellom ord (pause 7 prikker)
                time.sleep(7 * PRIKK_VARIGHET)
                continue

            # Pause mellom symboler i samme bokstav (1 prikk)
            # Unntatt etter siste symbol
            if symbol != morse_code[-1] and symbol != " ":
                time.sleep(PRIKK_VARIGHET)

        # Pause mellom bokstaver (3 prikker)
        time.sleep(3 * PRIKK_VARIGHET)

    # Oppgave 4: Blink et helt ord
    def blink_morse_word(self, word):
        """
        Blinker et helt ord i morse
        """
        print(f"Blinker ordet: {word}")
        for char in word:
            if char.upper() in MORSE:
                self.blink_morse_char(char.upper())
            else:
                print(f"Hopper over ugyldig tegn: {char}")

    # Oppgave 5: Blink en setning
    def blink_morse_sentence(self, sentence):
        """
        Blinker en hel setning i morse
        """
        # Del opp i ord (splitt på mellomrom)
        words = sentence.split()

        for i, word in enumerate(words):
            self.blink_morse_word(word)
            # Pause mellom ord (7 prikker) - unntatt etter siste ord
            if i < len(words) - 1:
                print("Pause mellom ord...")
                time.sleep(7 * PRIKK_VARIGHET)

    # Hjelpefunksjon for å validere tekst
    def validate_text(self, text):
        """
        Fjerner ugyldige tegn fra teksten
        """
        valid_chars = []
        for char in text:
            if char.upper() in MORSE or char == " ":
                valid_chars.append(char)
            else:
                print(f"Fjerner ugyldig tegn: {char}")

        return "".join(valid_chars)


def main():
    """
    Hovedprogram som kjører alle oppgavene
    """
    blinker = MorseBlinker(LED_PIN)

    try:
        # Oppgave 1: Blink i ett sekund
        print("\n--- Oppgave 1: Blink i 1 sekund ---")
        blinker.blink_one_second()
        time.sleep(1)

        # Oppgave 2: Blink to ganger
        print("\n--- Oppgave 2: Blink to ganger ---")
        blinker.blink_twice()
        time.sleep(1)

        # Oppgave 3: Test en bokstav
        print("\n--- Oppgave 3: Blink bokstaven 'S' ---")
        blinker.blink_morse_char("S")
        time.sleep(2)

        # Oppgave 3: Test en annen bokstav
        print("\n--- Oppgave 3: Blink bokstaven 'O' ---")
        blinker.blink_morse_char("O")
        time.sleep(2)

        # Oppgave 4: Test et ord
        print("\n--- Oppgave 4: Blink ordet 'SOS' ---")
        blinker.blink_morse_word("SOS")
        time.sleep(2)

        # Oppgave 5: Interaktiv modus
        print("\n--- Oppgave 5: Interaktiv morse-sending ---")
        print("Skriv inn tekst for å blinke i morse (Ctrl+C for å avslutte)")

        while True:
            text = input("\nSkriv inn tekst: ")
            if text.strip():
                validated = blinker.validate_text(text)
                if validated:
                    print(f"Blinker: {validated}")
                    blinker.blink_morse_sentence(validated)
                else:
                    print("Ingen gyldige tegn å blinke")
            else:
                print("Tom streng, prøv igjen")

    except KeyboardInterrupt:
        # Dette fanges av signal_handler, men vi har med som backup
        pass
    finally:
        blinker.cleanup()


if __name__ == "__main__":
    main()
