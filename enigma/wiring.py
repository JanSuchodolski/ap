ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_TO_INDEX = {ch: idx for idx, ch in enumerate(ALPHABET)}
INDEX_TO_ALPHABET = {idx: ch for idx, ch in enumerate(ALPHABET)}

ROTORS = {
	"I": {
		"wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
		"notch": "Q",
	},
	"II": {
		"wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
		"notch": "E",
	},
	"III": {
		"wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
		"notch": "V",
	},
	"IV": {
		"wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
		"notch": "J",
	},
	"V": {
		"wiring": "VZBRGITYUPSDNHLXAWMJQOFECK",
		"notch": "Z",
	},
}

REFLECTORS = {
	"B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
	"C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}