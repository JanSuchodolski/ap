# Maszyna Enigma – implementacja w Pythonie

Projekt zawiera kompletną implementację klasycznej maszyny Enigma (3-wirnikowej) z obsługą:
- wirników I–V z poprawnym mechanizmem podwójnego kroku,
- ustawień pierścienia (Ringstellung), pozycji startowych (Grundstellung),
- wtycznicy (plugboard),
- reflektorów B i C,
- generatora losowego klucza,
- prostego CLI oraz testów,
- logowania historii kroków i opcjonalnej wizualizacji Pygame.

## Instalacja

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Aby użyć Pygame (opcjonalnie):

```bash
# Linux: wymagane biblioteki SDL (np. libsdl2-dev) – w środowiskach CI często niedostępne
# Następnie:
pip install -e .[ui]
```

## Szybki start (CLI)

```bash
python enigma_cli.py encrypt --rotors I II III --rings AAA --positions AAA --reflector B "HELLOWORLD"
# -> ILBDAAMTAZ

python enigma_cli.py decrypt --rotors I II III --rings AAA --positions AAA --reflector B "ILBDAAMTAZ"
# -> HELLOWORLD

python enigma_cli.py genkey --rotors 3 --plugs 6
```

### Raport kroków

```bash
python enigma_cli.py encrypt --rotors I II III --rings AAA --positions AAA --reflector B --report "ABCDEF"
# wypisze szyfrogram i tabelę kroków (pozycje BEFORE/AFTER oraz które wirniki się przesunęły)
```

## API (Python)

```python
from enigma import EnigmaMachine, EnigmaConfig

config = EnigmaConfig(
    rotors=["I", "II", "III"],
    reflector="B",
    ring_settings="AAA",
    starting_positions="AAA",
    plugboard_pairs=["AB", "CD"],
)
machine = EnigmaMachine(config)

cipher = machine.encrypt("HELLOWORLD")
plain = EnigmaMachine(config).decrypt(cipher)

# Z historią
cipher2 = machine.encrypt_with_history("ABC")
print(machine.history_report())
```

## Pygame (opcjonalnie)

Uruchom prosty podgląd po instalacji extras:

```bash
pip install -e .[ui]
python enigma_pygame.py
```

- Wyświetla aktualne pozycje wirników (L→R) dla indeksu wpisanego tekstu
- Szyfruje „na żywo” podczas pisania
- ESC – wyjście, BACKSPACE – kasowanie znaku, SPACE – spacja

## Testy

```bash
pytest -q
```

## Uwagi implementacyjne
- Zaimplementowano podwójny krok zgodnie z historycznymi zasadami.
- Ustawienie pierścienia (Ringstellung) przesuwa mapowania wewnątrz wirnika przy przejściu w przód i wstecz.
- Deszyfrowanie jest identyczne jak szyfrowanie przy tych samych ustawieniach.