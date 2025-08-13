from __future__ import annotations

import json
import random
from dataclasses import asdict
from typing import List

from .machine import EnigmaConfig
from .wiring import ALPHABET, ROTORS, REFLECTORS


def generate_random_config(num_rotors: int = 3, num_plug_pairs: int | None = None) -> EnigmaConfig:
	if num_rotors < 3:
		raise ValueError("num_rotors must be at least 3")
	rotor_names = random.sample(list(ROTORS.keys()), k=num_rotors)
	ring_settings = "".join(random.choice(ALPHABET) for _ in range(num_rotors))
	starting_positions = "".join(random.choice(ALPHABET) for _ in range(num_rotors))
	reflector = random.choice(list(REFLECTORS.keys()))
	letters = list(ALPHABET)
	random.shuffle(letters)
	pairs: List[str] = []
	if num_plug_pairs is None:
		num_plug_pairs = random.randint(0, 10)
	num_plug_pairs = max(0, min(10, num_plug_pairs))
	if num_plug_pairs > 0:
		usable = letters.copy()
		pairs_left = num_plug_pairs
		while pairs_left > 0 and len(usable) >= 2:
			a = usable.pop()
			b = usable.pop()
			pairs.append(a + b)
			pairs_left -= 1
	return EnigmaConfig(
		rotors=rotor_names,
		reflector=reflector,
		ring_settings=ring_settings,
		starting_positions=starting_positions,
		plugboard_pairs=pairs,
	)


def config_to_json(config: EnigmaConfig) -> str:
	return json.dumps(asdict(config), ensure_ascii=False, indent=2)