from typing import Dict, Iterable, Tuple

from .wiring import ALPHABET_TO_INDEX


class Plugboard:
	def __init__(self, pairs: Iterable[Tuple[str, str]] | None = None) -> None:
		self.mapping: Dict[int, int] = {}
		if pairs:
			used: set[int] = set()
			for a, b in pairs:
				ai = ALPHABET_TO_INDEX[a]
				bi = ALPHABET_TO_INDEX[b]
				if ai in used or bi in used or ai == bi:
					raise ValueError("Invalid plugboard pair or duplicate letter")
				self.mapping[ai] = bi
				self.mapping[bi] = ai
				used.add(ai)
				used.add(bi)

	def map_index(self, index: int) -> int:
		return self.mapping.get(index, index)