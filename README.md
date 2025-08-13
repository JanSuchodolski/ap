# Maszyna Enigma – implementacja w Pythonie

Projekt zawiera kompletną implementację klasycznej maszyny Enigma (3-wirnikowej) z obsługą:
- wirników I–V z poprawnym mechanizmem podwójnego kroku,
- ustawień pierścienia (Ringstellung), pozycji startowych (Grundstellung),
- wtycznicy (plugboard),
- reflektorów B i C,
- generatora losowego klucza,
- prostego CLI oraz testów.

## Instalacja

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Szybki start (CLI)

```bash
python enigma_cli.py encrypt --rotors I II III --rings AAA --positions AAA --reflector B --text HELLOWORLD
# -> ILBDAAMTAZ

python enigma_cli.py decrypt --rotors I II III --rings AAA --positions AAA --reflector B --text ILBDAAMTAZ
# -> HELLOWORLD

python enigma_cli.py genkey --rotors 3 --plugs 6
```

Parametry:
- `--rotors` – nazwy wirników w kolejności od lewej do prawej (np. `I II III`).
- `--rings` – ustawienia pierścieni, np. `AAA`.
- `--positions` – pozycje startowe, np. `AAA`.
- `--reflector` – `B` lub `C`.
- `--plugs` – pary wtycznicy, np. `AB CD EF`.
- `--letters-only` – jeśli podane, znaki niebędące literami są odrzucane (domyślnie są zachowywane).

## API (Python)

```python
from enigma import EnigmaMachine, EnigmaConfig, generate_random_config

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
```

## Testy

```bash
pytest -q
```

## Uwagi implementacyjne
- Zaimplementowano podwójny krok zgodnie z historycznymi zasadami.
- Ustawienie pierścienia (Ringstellung) przesuwa mapowania wewnątrz wirnika przy przejściu w przód i wstecz.
- Deszyfrowanie jest identyczne jak szyfrowanie przy tych samych ustawieniach.