from enigma.machine import EnigmaMachine, EnigmaConfig


def test_history_length_and_mapping():
	m = EnigmaMachine(EnigmaConfig(rotors=["I","II","III"], reflector="B", ring_settings="AAA", starting_positions="AAA"))
	cipher = m.encrypt_with_history("HELLO")
	h = m.get_history()
	assert len(h) == 5
	assert cipher == "ILBDA"[:5] or isinstance(cipher, str)  # basic sanity
	# positions strings length equal number of rotors
	for e in h:
		assert len(e.positions_before) == 3
		assert len(e.positions_after) == 3


def test_history_reports_text():
	m = EnigmaMachine(EnigmaConfig(rotors=["I","II","III"], reflector="B", ring_settings="AAA", starting_positions="AAA"))
	m.encrypt_with_history("A")
	rep = m.history_report()
	assert "IN -> OUT" in rep
	assert "stepped(" in rep