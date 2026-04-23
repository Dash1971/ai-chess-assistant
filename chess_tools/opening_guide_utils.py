#!/usr/bin/env python3
"""Shared helpers for opening guide generators."""

from __future__ import annotations


def build_theme_hint(game):
    chapter = game.get('chapter', '')
    if not chapter:
        return ''
    chapter = chapter.strip()
    if chapter.startswith('(') and ')' in chapter:
        theme_hint = chapter[1:chapter.index(')')]
        return f' <span class="theme-hint">({theme_hint})</span>'
    return ''


def build_game_link(game, opponent_field, include_result_icon=False):
    opponent = game[opponent_field]
    url = game['url']
    theme_hint = build_theme_hint(game)
    result_icon = ''
    if include_result_icon:
        result_icon = ' ✓' if game['result'] == '0-1' else (' ½' if game['result'] == '1/2-1/2' else ' ✗')
    if url:
        return f'<a href="{url}">{opponent}</a>{result_icon}{theme_hint}'
    return f'{opponent}{result_icon}{theme_hint}'


def game_list_html(game_list, render_item, columns=2):
    """Generate a UL game list."""
    if not game_list:
        return '<p class="empty">No games found.</p>'
    rows = ''.join(f'<li>{render_item(g)}</li>' for g in game_list)
    col_class = f'columns: {columns};' if columns > 1 else ''
    return f'<ul class="game-list" style="{col_class}">{rows}</ul>'


def theme_box(title, description, game_list, render_item, columns=2):
    """Generate a themed game section."""
    if not game_list:
        return ''
    return f'''<div class="theme-group">
    <h4>{title} <span class="count">({len(game_list)} games)</span></h4>
    <p class="theme-desc">{description}</p>
    {game_list_html(game_list, render_item, columns)}
    </div>'''

