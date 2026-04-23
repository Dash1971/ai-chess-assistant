#!/usr/bin/env python3
"""Shared helpers for opening taggers."""

from __future__ import annotations

import re


def get_raw_text(pgn_path, chapter_url):
    """Get full raw text for a game by chapter URL."""
    with open(pgn_path) as f:
        content = f.read()
    games = re.split(r'\n\n(?=\[Event)', content)
    for g in games:
        if chapter_url and chapter_url in g:
            return g
    return ''


def get_annotations(raw_text):
    """Extract all annotation comments from raw game text."""
    return ' '.join(re.findall(r'\{([^}]*)\}', raw_text))


def has_move_early(moves, pattern, max_move=15):
    """Check if a move pattern appears in the first N moves."""
    for num, move in moves:
        if num > max_move:
            break
        if re.match(pattern, move):
            return True
    return False


def has_move_any(moves, pattern):
    """Check if a move appears anywhere in the game."""
    for _num, move in moves:
        if re.match(pattern, move):
            return True
    return False


def move_number_of(moves, pattern, max_move=999):
    """Return the move number of first occurrence of pattern, or 0."""
    for num, move in moves:
        if num > max_move:
            break
        if re.match(pattern, move):
            return num
    return 0


def first_n_moves_set(moves, n=10):
    """Return set of move strings from the first N moves."""
    return {m for num, m in moves if num <= n}

