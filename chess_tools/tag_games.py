#!/usr/bin/env python3
"""
Tag wonestall Stonewall games with thematic categories.
Outputs /tmp/sw_data.json for generate_pdf.py consumption.

IMPORTANT: Thematic tags are based on the OPENING PHASE (first 15 moves)
to avoid false positives from random middlegame/endgame moves.
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_pgn import load_games
from stonewall_rules import tag_white_game, tag_black_game
from opening_tag_pipeline import print_tag_summary, tag_game_collection, write_tag_output
from stonewall_opening_data import DEFAULT_PGN, DEFAULT_TAG_OUTPUT, MOVE_CUTOFF

PGN = os.environ.get('OPENING_PGN_PATH', str(DEFAULT_PGN))
OUTPUT_JSON = os.environ.get('OPENING_TAG_OUTPUT', str(DEFAULT_TAG_OUTPUT))






def run(pgn_path=PGN, output_json=OUTPUT_JSON, quiet=False):
    white_games, black_games = load_games(pgn_path, 'wonestall')

    # Tag white games
    tag_game_collection(white_games, pgn_path, tag_white_game)

    # Tag black games
    tag_game_collection(black_games, pgn_path, tag_black_game)

    # Output stats
    if not quiet:
        print(f"Tagged {len(white_games)} white + {len(black_games)} black games")
        print(f"(Opening cutoff: {MOVE_CUTOFF} moves)")

    print_tag_summary('White tags', white_games, quiet=quiet)
    print_tag_summary('Black tags', black_games, quiet=quiet)

    # Write JSON
    data = {
        'white_games': white_games,
        'black_games': black_games,
    }
    write_tag_output(data, output_json, quiet=quiet)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Tag Stonewall games with thematic categories.')
    parser.add_argument('--db', default=PGN, help='Path to PGN database')
    parser.add_argument('--output', default=OUTPUT_JSON, help='Path to output JSON')
    parser.add_argument('--quiet', action='store_true', help='Reduce stats output')
    args = parser.parse_args(argv)
    run(pgn_path=args.db, output_json=args.output, quiet=args.quiet)


if __name__ == '__main__':
    main()
