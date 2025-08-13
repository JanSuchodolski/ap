#!/usr/bin/env python3
from __future__ import annotations

import sys
import pygame

from enigma.machine import EnigmaMachine, EnigmaConfig

WIDTH, HEIGHT = 640, 360
BG = (24, 24, 28)
FG = (230, 230, 230)
ACCENT = (120, 190, 255)
MUTED = (170, 170, 170)


def draw_text(surface, text, pos, font, color=FG):
	img = font.render(text, True, color)
	surface.blit(img, pos)


def main() -> int:
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Enigma – Pygame")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("monospace", 22)
	small = pygame.font.SysFont("monospace", 16)

	config = EnigmaConfig(
		rotors=["I", "II", "III"],
		reflector="B",
		ring_settings="AAA",
		starting_positions="AAA",
		plugboard_pairs=["AB", "CD", "EF"],
	)
	machine = EnigmaMachine(config)

	typed = ""
	cipher = ""

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return 0
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					return 0
				elif event.key == pygame.K_BACKSPACE:
					if typed:
						typed = typed[:-1]
						cipher = cipher[:-1]
				elif event.key == pygame.K_SPACE:
					typed += " "
					cipher += " "
				else:
					ch = event.unicode.upper()
					if ch.isalpha() and len(ch) == 1:
						# Use a fresh machine for stateless per-key encryption visualization
						m = EnigmaMachine(config)
						# Advance positions based on already typed letters (letters only)
						m.encrypt("".join(c for c in typed if c.isalpha()))
						enc = m.encrypt(ch)
						typed += ch
						cipher += enc

		screen.fill(BG)

		# Titles
		draw_text(screen, "Enigma – Pygame podgląd", (20, 16), font, ACCENT)

		# Rotor positions preview for a fresh machine at current index
		m_preview = EnigmaMachine(config)
		m_preview.encrypt("".join(c for c in typed if c.isalpha()))
		positions = m_preview._positions_letters()  # type: ignore[attr-defined]
		draw_text(screen, f"Pozycje wirników (L→R): {positions}", (20, 56), small, MUTED)

		# Inputs/outputs
		draw_text(screen, "Wejście:", (20, 100), small, MUTED)
		draw_text(screen, typed, (20, 124), font, FG)
		draw_text(screen, "Wyjście:", (20, 168), small, MUTED)
		draw_text(screen, cipher, (20, 192), font, FG)

		# Help
		draw_text(screen, "ESC – wyjście, BACKSPACE – kasuj, SPACE – spacja", (20, HEIGHT - 36), small, MUTED)

		pygame.display.flip()
		clock.tick(60)


if __name__ == "__main__":
	sys.exit(main())