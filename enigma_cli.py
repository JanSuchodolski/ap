#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from typing import List

from enigma.machine import EnigmaMachine, EnigmaConfig
from enigma.keygen import generate_random_config, config_to_json


def parse_pairs(pairs_list: List[str] | None) -> List[str] | None:
	if not pairs_list:
		return None
	pairs: List[str] = []
	for item in pairs_list:
		pair = item.strip().upper()
		if len(pair) != 2 or not pair.isalpha():
			raise argparse.ArgumentTypeError("Plugboard pairs must be two letters like AB")
		pairs.append(pair)
	return pairs


def parse_args(argv: List[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Enigma Machine CLI")
	sub = parser.add_subparsers(dest="cmd", required=True)

	enc = sub.add_parser("encrypt", help="Encrypt text")
	enc.add_argument("text", help="Text to process")
	enc.add_argument("--rotors", nargs="+", required=True, help="Rotor names in order Left->Right, e.g. I II III")
	enc.add_argument("--rings", required=True, help="Ring settings string, e.g. AAA")
	enc.add_argument("--positions", required=True, help="Starting positions string, e.g. AAA")
	enc.add_argument("--reflector", required=True, help="Reflector name, e.g. B")
	enc.add_argument("--plugs", nargs="*", help="Plugboard pairs like AB CD EF")
	enc.add_argument("--letters-only", action="store_true", help="Drop non-letters instead of preserving them")
	enc.add_argument("--report", action="store_true", help="Print step history report")

	dec = sub.add_parser("decrypt", help="Decrypt text (same as encrypt with same config)")
	dec.add_argument("text", help="Text to process")
	dec.add_argument("--rotors", nargs="+", required=True, help="Rotor names in order Left->Right, e.g. I II III")
	dec.add_argument("--rings", required=True, help="Ring settings string, e.g. AAA")
	dec.add_argument("--positions", required=True, help="Starting positions string, e.g. AAA")
	dec.add_argument("--reflector", required=True, help="Reflector name, e.g. B")
	dec.add_argument("--plugs", nargs="*", help="Plugboard pairs like AB CD EF")
	dec.add_argument("--letters-only", action="store_true", help="Drop non-letters instead of preserving them")
	dec.add_argument("--report", action="store_true", help="Print step history report")

	gen = sub.add_parser("genkey", help="Generate a random configuration")
	gen.add_argument("--rotors", type=int, default=3, help="Number of rotors (>=3)")
	gen.add_argument("--plugs", type=int, default=None, help="Number of plugboard pairs (0..10)")

	return parser.parse_args(argv)


def main(argv: List[str]) -> int:
	args = parse_args(argv)
	if args.cmd == "genkey":
		config = generate_random_config(num_rotors=args.rotors, num_plug_pairs=args.plugs)
		print(config_to_json(config))
		return 0

	pairs = parse_pairs(args.plugs)
	config = EnigmaConfig(
		rotors=[r.upper() for r in args.rotors],
		reflector=args.reflector.upper(),
		ring_settings=args.rings.upper(),
		starting_positions=args.positions.upper(),
		plugboard_pairs=pairs,
	)
	machine = EnigmaMachine(config)
	preserve = not getattr(args, "letters_only", False) is True
	if args.cmd == "encrypt":
		if getattr(args, "report", False):
			cipher = machine.encrypt_with_history(args.text, preserve_non_letters=not args.letters_only)
			print(cipher)
			print(machine.history_report())
			return 0
		else:
			print(machine.encrypt(args.text, preserve_non_letters=not args.letters_only))
			return 0
	elif args.cmd == "decrypt":
		if getattr(args, "report", False):
			plain = machine.encrypt_with_history(args.text, preserve_non_letters=not args.letters_only)
			print(plain)
			print(machine.history_report())
			return 0
		else:
			print(machine.decrypt(args.text, preserve_non_letters=not args.letters_only))
			return 0
	return 1


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))