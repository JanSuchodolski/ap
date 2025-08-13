from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from .rotor import Rotor, build_rotor
from .plugboard import Plugboard
from .wiring import ALPHABET, ALPHABET_TO_INDEX, INDEX_TO_ALPHABET, ROTORS, REFLECTORS


@dataclass
class EnigmaConfig:
	rotors: List[str]
	reflector: str
	ring_settings: str
	starting_positions: str
	plugboard_pairs: List[str] | None = None

	def validate(self) -> None:
		if len(self.rotors) < 3:
			raise ValueError("At least 3 rotors required")
		if len(self.ring_settings) != len(self.rotors):
			raise ValueError("Ring settings length must match number of rotors")
		if len(self.starting_positions) != len(self.rotors):
			raise ValueError("Starting positions length must match number of rotors")
		for r in self.rotors:
			if r not in ROTORS:
				raise ValueError(f"Unknown rotor: {r}")
		if self.reflector not in REFLECTORS:
			raise ValueError(f"Unknown reflector: {self.reflector}")
		if self.plugboard_pairs:
			seen: set[str] = set()
			for pair in self.plugboard_pairs:
				if len(pair) != 2:
					raise ValueError("Plugboard pairs must be two letters like 'AB'")
				A, B = pair[0], pair[1]
				if A == B:
					raise ValueError("Plugboard pair cannot map a letter to itself")
				if A in seen or B in seen:
					raise ValueError("Plugboard letter used more than once")
				seen.add(A)
				seen.add(B)


class EnigmaMachine:
	def __init__(
		self,
		config: EnigmaConfig,
	) -> None:
		config.validate()
		self.rotors: List[Rotor] = self._build_rotors(config.rotors, config.ring_settings, config.starting_positions)
		self.reflector_map = [ALPHABET_TO_INDEX[ch] for ch in REFLECTORS[config.reflector]]
		pairs: List[Tuple[str, str]] = []
		if config.plugboard_pairs:
			pairs = [(p[0], p[1]) for p in config.plugboard_pairs]
		self.plugboard = Plugboard(pairs)

	def _build_rotors(self, rotor_names: Iterable[str], ring_settings: str, starting_positions: str) -> List[Rotor]:
		rotors: List[Rotor] = []
		for name, ring_letter, start_letter in zip(rotor_names, ring_settings, starting_positions):
			data = ROTORS[name]
			rotors.append(build_rotor(name, data["wiring"], data["notch"], ring_letter, start_letter))
		return rotors  # left to right order, as supplied

	def _step_rotors(self) -> None:
		# Assume exactly three rotors for classic Enigma order: [Left, Middle, Right]
		left, middle, right = self.rotors[-3], self.rotors[-2], self.rotors[-1]
		middle_at_notch = middle.at_notch()
		right_at_notch = right.at_notch()

		if middle_at_notch:
			left.step()
		if right_at_notch or middle_at_notch:
			middle.step()
		right.step()

	def _encode_index(self, index: int) -> int:
		self._step_rotors()
		# Plugboard in
		index = self.plugboard.map_index(index)
		# Through rotors forward: Right -> ... -> Left
		for rotor in reversed(self.rotors):
			index = rotor.encode_forward(index)
		# Reflector
		index = self.reflector_map[index]
		# Through rotors backward: Left -> ... -> Right
		for rotor in self.rotors:
			index = rotor.encode_backward(index)
		# Plugboard out
		index = self.plugboard.map_index(index)
		return index

	def encrypt(self, text: str, *, preserve_non_letters: bool = True) -> str:
		result_chars: List[str] = []
		for ch in text:
			if ch.upper() in ALPHABET:
				idx = ALPHABET_TO_INDEX[ch.upper()]
				enc_idx = self._encode_index(idx)
				result_chars.append(INDEX_TO_ALPHABET[enc_idx])
			elif preserve_non_letters:
				result_chars.append(ch)
			# else: skip non-letters
		return "".join(result_chars)

	def decrypt(self, text: str, *, preserve_non_letters: bool = True) -> str:
		return self.encrypt(text, preserve_non_letters=preserve_non_letters)