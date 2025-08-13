from enigma.machine import EnigmaMachine, EnigmaConfig


def build_machine(rotors, rings, positions, reflector, plugs=None):
	return EnigmaMachine(EnigmaConfig(rotors=rotors, ring_settings=rings, starting_positions=positions, reflector=reflector, plugboard_pairs=plugs))


def test_roundtrip_simple():
	m1 = build_machine(["I", "II", "III"], "AAA", "AAA", "B")
	plaintext = "HELLOWORLD"
	cipher = m1.encrypt(plaintext)
	m2 = build_machine(["I", "II", "III"], "AAA", "AAA", "B")
	assert m2.decrypt(cipher) == plaintext


def test_known_vector_helloworld():
	m = build_machine(["I", "II", "III"], "AAA", "AAA", "B")
	assert m.encrypt("HELLOWORLD") == "ILBDAAMTAZ"


def test_known_vector_AAAAA():
	m = build_machine(["I", "II", "III"], "AAA", "AAA", "B")
	assert m.encrypt("AAAAA") == "BDZGO"


def test_plugboard_roundtrip():
	m1 = build_machine(["I", "II", "III"], "AAA", "AAA", "B", plugs=["AB", "CD", "EF"]) 
	text = "ENIGMA MACHINE TEST"
	cipher = m1.encrypt(text)
	m2 = build_machine(["I", "II", "III"], "AAA", "AAA", "B", plugs=["AB", "CD", "EF"]) 
	assert m2.decrypt(cipher) == "ENIGMA MACHINE TEST"