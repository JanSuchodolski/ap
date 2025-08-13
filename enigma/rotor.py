from dataclasses import dataclass
from typing import List

from .wiring import ALPHABET, ALPHABET_TO_INDEX, INDEX_TO_ALPHABET


@dataclass
class Rotor:
	name: str
	wiring_forward: List[int]
	wiring_backward: List[int]
	notch_index: int
	ring_setting: int
	position: int

	def at_notch(self) -> bool:
		return self.position == self.notch_index

	def step(self) -> None:
		self.position = (self.position + 1) % 26

	def encode_forward(self, input_index: int) -> int:
		shifted = (input_index + self.position - self.ring_setting) % 26
		mapped = self.wiring_forward[shifted]
		return (mapped - self.position + self.ring_setting) % 26

	def encode_backward(self, input_index: int) -> int:
		shifted = (input_index + self.position - self.ring_setting) % 26
		mapped = self.wiring_backward[shifted]
		return (mapped - self.position + self.ring_setting) % 26


def build_rotor(name: str, wiring: str, notch: str, ring_letter: str, start_letter: str) -> Rotor:
	wiring_forward = [ALPHABET_TO_INDEX[ch] for ch in wiring]
	wiring_backward = [0] * 26
	for i, out_idx in enumerate(wiring_forward):
		wiring_backward[out_idx] = i
	notch_index = ALPHABET_TO_INDEX[notch]
	ring_setting = ALPHABET_TO_INDEX[ring_letter]
	position = ALPHABET_TO_INDEX[start_letter]
	return Rotor(
		name=name,
		wiring_forward=wiring_forward,
		wiring_backward=wiring_backward,
		notch_index=notch_index,
		ring_setting=ring_setting,
		position=position,
	)