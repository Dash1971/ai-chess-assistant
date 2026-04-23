#!/usr/bin/env python3
"""Shared execution helpers for opening taggers."""

from __future__ import annotations

import json
from collections import Counter

from opening_tag_utils import get_raw_text


def tag_game_collection(games, pgn_path, tagger, postprocess=None):
    """Tag a collection of games in-place and return it."""
    for game in games:
        raw = get_raw_text(pgn_path, game.get('url'))
        game['tags'] = tagger(game, raw)
        if postprocess:
            postprocess(game, raw)
    return games


def count_tags(games):
    counts = Counter()
    for game in games:
        for tag in game.get('tags', []):
            counts[tag] += 1
    return counts


def print_tag_summary(label, games, quiet=False):
    if quiet:
        return
    print(f"\n{label}:")
    for tag, count in sorted(count_tags(games).items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count}")


def write_tag_output(data, output_json, quiet=False):
    with open(output_json, 'w') as f:
        json.dump(data, f, default=str)
    if not quiet:
        print(f"\nWrote {output_json}")

