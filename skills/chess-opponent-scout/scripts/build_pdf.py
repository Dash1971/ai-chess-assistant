#!/usr/bin/env python3
"""Build a polished scouting-report PDF from chess-opponent-scout analysis.json."""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
WORKSPACE = HERE.parents[3]
for candidate in [
    WORKSPACE / ".venvs/chess-workbook/lib/python3.12/site-packages",
]:
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

DARK = HexColor("#172033")
ACCENT = HexColor("#5b21b6")
ACCENT_2 = HexColor("#0f766e")
ACCENT_LIGHT = HexColor("#f5f3ff")
MUTED = HexColor("#667085")
LIGHT = HexColor("#f8fafc")
BORDER = HexColor("#d0d5dd")
GOOD = HexColor("#166534")
WARN = HexColor("#92400e")
BAD = HexColor("#991b1b")

styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=25,
    leading=31,
    textColor=DARK,
    alignment=TA_CENTER,
    spaceAfter=6,
)
SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=10,
    leading=13,
    textColor=MUTED,
    alignment=TA_CENTER,
    spaceAfter=12,
)
DECK = ParagraphStyle(
    "Deck",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11.5,
    leading=15,
    textColor=DARK,
    alignment=TA_CENTER,
    spaceAfter=16,
)
H1 = ParagraphStyle(
    "H1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=20,
    textColor=ACCENT,
    spaceBefore=12,
    spaceAfter=6,
)
H2 = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11.5,
    leading=14,
    textColor=ACCENT_2,
    spaceBefore=8,
    spaceAfter=4,
)
BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    textColor=DARK,
    alignment=TA_JUSTIFY,
    spaceAfter=5,
)
BODY_LEFT = ParagraphStyle("BodyLeft", parent=BODY, alignment=TA_LEFT)
SMALL = ParagraphStyle("Small", parent=BODY_LEFT, fontSize=8.4, leading=10.6, textColor=MUTED)
TINY = ParagraphStyle("Tiny", parent=BODY_LEFT, fontSize=7.8, leading=9.4, textColor=MUTED)
CALLOUT = ParagraphStyle(
    "Callout",
    parent=BODY_LEFT,
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14,
    textColor=DARK,
)
TABLE_CELL = ParagraphStyle("TableCell", parent=BODY_LEFT, fontSize=8.7, leading=10.7)
TABLE_HEAD = ParagraphStyle("TableHead", parent=TABLE_CELL, fontName="Helvetica-Bold", textColor=colors.white)
FOOTER = ParagraphStyle("Footer", parent=TINY, alignment=TA_RIGHT)
EYEBROW = ParagraphStyle(
    "Eyebrow",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.8,
    leading=10,
    textColor=ACCENT,
    alignment=TA_CENTER,
    spaceAfter=6,
)


def fmt_pct(value: float | int | None) -> str:
    if value is None:
        return "—"
    return f"{value:.1f}%"


def fmt_num(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        if math.isclose(value, round(value), abs_tol=1e-9):
            return str(int(round(value)))
        return f"{value:.1f}"
    return str(value)


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def score_band(score: float | None) -> str:
    if score is None:
        return "unknown"
    if score >= 55:
        return "strong"
    if score >= 48:
        return "serviceable"
    return "weak"


def table(data, widths, header_bg=ACCENT, zebra=True, align="LEFT"):
    tbl = Table(data, colWidths=widths, hAlign=align)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.6),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if zebra and len(data) > 1:
        for row in range(1, len(data)):
            if row % 2 == 1:
                style.append(("BACKGROUND", (0, row), (-1, row), LIGHT))
    tbl.setStyle(TableStyle(style))
    return tbl


def card(title: str, body: str, width: float = 2.17 * inch):
    content = [
        [Paragraph(title, ParagraphStyle("CardHead", parent=TABLE_HEAD, alignment=TA_CENTER))],
        [Paragraph(body, ParagraphStyle("CardBody", parent=BODY_LEFT, alignment=TA_CENTER, fontSize=11, leading=14, spaceAfter=0))],
    ]
    tbl = Table(content, colWidths=[width], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("BACKGROUND", (0, 1), (0, 1), ACCENT_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def section_banner(title: str, subtitle: str | None = None):
    rows = [[Paragraph(title, ParagraphStyle("BannerTitle", parent=H1, textColor=colors.white, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0))]]
    if subtitle:
        rows.append([Paragraph(subtitle, ParagraphStyle("BannerSub", parent=SMALL, textColor=colors.white, alignment=TA_LEFT))])
    tbl = Table(rows, colWidths=[6.35 * inch], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("BOX", (0, 0), (-1, -1), 0.6, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def info_strip(items: list[tuple[str, str]]):
    data = [[Paragraph(f"<b>{k}</b><br/>{v}", ParagraphStyle("Strip", parent=BODY_LEFT, alignment=TA_CENTER, textColor=DARK, fontSize=9, leading=12, spaceAfter=0)) for k, v in items]]
    tbl = Table(data, colWidths=[6.35 * inch / max(1, len(items))] * max(1, len(items)), hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def bullet_block(lines: list[str]) -> Paragraph:
    if not lines:
        lines = ["No significant data."]
    return Paragraph("<br/>".join(f"• {line}" for line in lines), BODY_LEFT)


def p(text: str, style=BODY_LEFT):
    return Paragraph(text, style)


def candidate_pools(tc_perf: dict[str, Any]):
    preferred = [k for k in ["bullet", "blitz", "rapid", "classical"] if k in tc_perf and tc_perf[k].get("games", 0) >= 10]
    if preferred:
        return [(k, tc_perf[k].get("score", 0), tc_perf[k].get("games", 0)) for k in preferred]
    broad = [(k, v.get("score", 0), v.get("games", 0)) for k, v in tc_perf.items() if v.get("games", 0) >= 10]
    if broad:
        return broad
    return [(k, v.get("score", 0), v.get("games", 0)) for k, v in tc_perf.items()]


def best_pool_label(tc_perf: dict[str, Any]) -> str:
    items = candidate_pools(tc_perf)
    if not items:
        return "—"
    k, score, games = max(items, key=lambda x: x[1])
    return f"{k} ({score:.1f}% over {games} games)"


def weakest_pool_label(tc_perf: dict[str, Any]) -> str:
    items = candidate_pools(tc_perf)
    if not items:
        return "—"
    k, score, games = min(items, key=lambda x: x[1])
    return f"{k} ({score:.1f}% over {games} games)"


def top_family(data: dict[str, Any], reverse=True, min_games=10):
    items = [(k, v) for k, v in data.items() if v.get("games", 0) >= min_games]
    if not items:
        items = list(data.items())
    if not items:
        return None, None
    return sorted(items, key=lambda kv: kv[1].get("score", 0), reverse=reverse)[0]


def join_date_text(profile: dict[str, Any], platform: str) -> str:
    try:
        if platform == "chesscom" and profile.get("joined"):
            return datetime.fromtimestamp(profile["joined"]).strftime("%Y-%m-%d")
        if platform == "lichess" and profile.get("createdAt"):
            return datetime.fromtimestamp(profile["createdAt"] / 1000).strftime("%Y-%m-%d")
    except Exception:
        pass
    return "—"


def synthesized_trend_text(analysis: dict[str, Any]) -> str:
    by_tc = analysis.get("improvement_profile", {}).get("by_time_control", {})
    if not by_tc:
        return "No clear improvement read."
    strong = [k for k, v in by_tc.items() if v.get("classification", {}).get("tier") in {"strong improver", "outlier improver"}]
    weak = [k for k, v in by_tc.items() if v.get("classification", {}).get("tier") == "plateau / below-average improver"]
    if strong and weak:
        return f"Split signal: strong improvement in {', '.join(strong)} but flat/negative trend in {', '.join(weak)}."
    pref = analysis.get("improvement_profile", {}).get("preferred")
    pref_label = analysis.get("improvement_profile", {}).get("preferred_time_control")
    if pref and pref_label:
        return (
            f"Main trend read: {pref_label} shows {pref.get('classification', {}).get('tier', 'unknown trend')} "
            f"({pref.get('classification', {}).get('estimated_percentile_band', 'no percentile estimate')})."
        )
    return "No clear improvement read."


def build_executive_summary(analysis: dict[str, Any]) -> list[str]:
    tc_perf = analysis.get("tc_performance", {})
    best = best_pool_label(tc_perf)
    worst = weakest_pool_label(tc_perf)
    white_top_name, white_top = top_family(analysis.get("eco_white", {}), reverse=True)
    black_weak_name, black_weak = top_family(analysis.get("eco_black", {}), reverse=False)

    lines = [
        f"Overall score is {analysis.get('score_rate', 0):.1f}% across {analysis.get('total', 0)} public games.",
        f"Best main pool: {best}. Weakest main pool: {worst}.",
    ]
    if white_top_name and white_top:
        lines.append(f"Best established White family is {white_top_name} at {white_top.get('score', 0):.1f}% over {white_top.get('games', 0)} games.")
    if black_weak_name and black_weak:
        lines.append(f"Most targetable Black family is {black_weak_name} at {black_weak.get('score', 0):.1f}% over {black_weak.get('games', 0)} games.")
    lines.append(synthesized_trend_text(analysis))
    if analysis.get("platform") == "lichess":
        bots = analysis.get("vs_bots", {}).get("games", 0)
        total = analysis.get("total", 0)
        if total and bots / total > 0.25:
            lines.append(f"Sample warning: bot share is {bots}/{total}, so some pattern confidence should be discounted slightly against humans.")
    return lines[:5]


def build_cover(story, analysis_path: Path, analysis: dict[str, Any]):
    username = analysis.get("username", analysis_path.parent.name)
    platform = analysis.get("platform", "—")
    profile = analysis.get("profile", {})
    created = join_date_text(profile, platform)
    deck = f"Public-game dossier for <b>{username}</b> on {platform}. Built from {analysis.get('total', 0)} games and tuned for practical prep, not vanity stats."

    story.append(Spacer(1, 0.22 * inch))
    story.append(Paragraph("OPPONENT SCOUT DOSSIER", EYEBROW))
    story.append(Paragraph(f"Scouting Report — {username}", TITLE))
    story.append(Paragraph(deck, DECK))
    story.append(Paragraph(
        f"Generated from public games only · Source file: {analysis_path.name} · Account created/joined: {created}",
        SUBTITLE,
    ))
    story.append(HRFlowable(width="84%", thickness=1, color=ACCENT, lineCap='round', spaceBefore=2, spaceAfter=14))
    story.append(info_strip([
        ("Platform", analysis.get("platform", "—")),
        ("Sample", f"{analysis.get('total', 0)} games"),
        ("White / Black", f"{analysis.get('white_win_rate', 0):.1f}% / {analysis.get('black_win_rate', 0):.1f}% wins"),
    ]))
    story.append(Spacer(1, 10))

    cards = Table([
        [
            card("Overall score", fmt_pct(analysis.get("score_rate"))),
            card("Best main pool", best_pool_label(analysis.get("tc_performance", {}))),
            card("Trend signal", synthesized_trend_text(analysis)),
        ]
    ], colWidths=[2.17 * inch, 2.17 * inch, 2.17 * inch])
    cards.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(cards)
    story.append(Spacer(1, 12))
    story.append(section_banner("Executive summary", "The fast read: where this player scores, where they bleed, and how their trend line behaves."))
    story.append(Spacer(1, 8))
    story.append(bullet_block(build_executive_summary(analysis)))
    story.append(PageBreak())


def build_profile_snapshot(story, analysis: dict[str, Any]):
    story.append(section_banner("Profile snapshot", "Baseline performance, pool split, and sample quality."))
    story.append(Spacer(1, 8))
    profile = analysis.get("profile", {})
    tc_perf = analysis.get("tc_performance", {})
    rows = [["Metric", "Value"]]
    rows.extend([
        ["Platform", analysis.get("platform", "—")],
        ["Games in sample", fmt_num(analysis.get("total"))],
        ["Overall score", fmt_pct(analysis.get("score_rate"))],
        ["White win rate", fmt_pct(analysis.get("white_win_rate"))],
        ["Black win rate", fmt_pct(analysis.get("black_win_rate"))],
        ["Best main pool", best_pool_label(tc_perf)],
        ["Weakest main pool", weakest_pool_label(tc_perf)],
        ["Draw rate", fmt_pct(analysis.get("draw_rate"))],
        ["Followers / rated count", fmt_num(profile.get("followers") if analysis.get("platform") == "chesscom" else analysis.get("rated_count"))],
    ])
    story.append(table(rows, [2.15 * inch, 4.35 * inch]))
    lines = [
        f"Overall score rate: {analysis.get('score_rate', 0):.1f}% across {analysis.get('total', 0)} games.",
        f"As White: {analysis.get('white_win_rate', 0):.1f}% wins. As Black: {analysis.get('black_win_rate', 0):.1f}% wins.",
    ]
    if analysis.get("platform") == "lichess":
        rated = analysis.get("rated_performance")
        casual = analysis.get("casual_performance")
        humans = analysis.get("vs_humans")
        bots = analysis.get("vs_bots")
        if rated and casual:
            lines.append(f"Rated score is {rated.get('score', 0):.1f}% vs casual {casual.get('score', 0):.1f}%.")
        if humans and bots:
            lines.append(f"Vs humans: {humans.get('score', 0):.1f}% score. Vs bots: {bots.get('score', 0):.1f}% score.")
    story.append(Spacer(1, 8))
    story.append(bullet_block(lines))


def build_repertoire(story, analysis: dict[str, Any]):
    story.append(section_banner("Opening repertoire", "What they actually play as White and how they answer the major first moves as Black."))
    story.append(Spacer(1, 8))

    white_first = analysis.get("first_move_white", [])
    resp_e4 = analysis.get("response_to_e4", [])
    resp_d4 = analysis.get("response_to_d4", [])
    white_best_name, white_best = top_family(analysis.get("eco_white", {}), reverse=True)
    white_worst_name, white_worst = top_family(analysis.get("eco_white", {}), reverse=False)
    black_best_name, black_best = top_family(analysis.get("eco_black", {}), reverse=True)
    black_worst_name, black_worst = top_family(analysis.get("eco_black", {}), reverse=False)

    white_lines = []
    if white_first:
        white_lines.append("First-move split: " + ", ".join(f"{m} ({n})" for m, n in white_first[:5]))
    if white_best_name and white_best:
        white_lines.append(f"Best established White family: {white_best_name} at {white_best.get('score', 0):.1f}% over {white_best.get('games', 0)} games.")
    if white_worst_name and white_worst:
        white_lines.append(f"Weakest established White family: {white_worst_name} at {white_worst.get('score', 0):.1f}% over {white_worst.get('games', 0)} games.")

    black_lines = []
    if resp_e4:
        black_lines.append("Vs 1.e4: " + ", ".join(f"{m} ({n})" for m, n in resp_e4[:5]))
    if resp_d4:
        black_lines.append("Vs 1.d4: " + ", ".join(f"{m} ({n})" for m, n in resp_d4[:5]))
    if black_best_name and black_best:
        black_lines.append(f"Best established Black family: {black_best_name} at {black_best.get('score', 0):.1f}% over {black_best.get('games', 0)} games.")
    if black_worst_name and black_worst:
        black_lines.append(f"Most targetable Black family: {black_worst_name} at {black_worst.get('score', 0):.1f}% over {black_worst.get('games', 0)} games.")

    split = Table([
        [Paragraph("White repertoire", H2), Paragraph("Black repertoire", H2)],
        [bullet_block(white_lines), bullet_block(black_lines)],
    ], colWidths=[3.2 * inch, 3.2 * inch])
    split.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(split)

    story.append(Spacer(1, 8))
    rows = [["Family", "Side", "Games", "Score", "Band"]]
    for side, fams in [("White", analysis.get("eco_white", {})), ("Black", analysis.get("eco_black", {}))]:
        top = sorted(fams.items(), key=lambda kv: kv[1].get("games", 0), reverse=True)[:6]
        for name, stats in top:
            rows.append([name, side, fmt_num(stats.get("games")), fmt_pct(stats.get("score")), score_band(stats.get("score"))])
    story.append(table(rows, [2.95 * inch, 0.65 * inch, 0.55 * inch, 0.7 * inch, 1.1 * inch]))


def build_style_and_time_controls(story, analysis: dict[str, Any]):
    story.append(section_banner("Format and style profile", "Where the points come from: pool strength, decision speed, and finish patterns."))
    story.append(Spacer(1, 8))
    rows = [["Pool", "Games", "Score", "Wins", "Draws", "Losses", "Read"]]
    for label in ["bullet", "blitz", "rapid", "classical", "daily", "correspondence"]:
        stats = analysis.get("tc_performance", {}).get(label)
        if not stats:
            continue
        rows.append([
            label,
            fmt_num(stats.get("games")),
            fmt_pct(stats.get("score")),
            fmt_num(stats.get("win")),
            fmt_num(stats.get("draw")),
            fmt_num(stats.get("loss")),
            score_band(stats.get("score")),
        ])
    story.append(table(rows, [1.0 * inch, 0.6 * inch, 0.72 * inch, 0.6 * inch, 0.6 * inch, 0.62 * inch, 1.0 * inch]))

    cw = analysis.get("castling_white", {})
    cb = analysis.get("castling_black", {})
    wb = analysis.get("win_by", {})
    lb = analysis.get("loss_by", {})
    lines = [
        f"White castling: K-side {cw.get('kingside', 0)}, Q-side {cw.get('queenside', 0)}, no castle {cw.get('none', 0)}.",
        f"Black castling: K-side {cb.get('kingside', 0)}, Q-side {cb.get('queenside', 0)}, no castle {cb.get('none', 0)}.",
        "Win modes: " + ", ".join(f"{k} {v}" for k, v in sorted(wb.items())),
        "Loss modes: " + ", ".join(f"{k} {v}" for k, v in sorted(lb.items())),
    ]
    if analysis.get("avg_game_length") is not None:
        lines.append(f"Average game length: {analysis.get('avg_game_length'):.1f} plies.")
    story.append(Spacer(1, 8))
    story.append(bullet_block(lines))


def improvement_row(label: str, entry: dict[str, Any]):
    series = entry.get("series", {})
    cls = entry.get("classification", {})
    return [
        label,
        fmt_num(series.get("start_rating")),
        fmt_num(series.get("latest_rating")),
        fmt_num(series.get("net_gain")),
        cls.get("tier", "—"),
        cls.get("estimated_percentile_band", "—"),
        entry.get("research_fit", "—"),
    ]


def build_improvement(story, analysis: dict[str, Any]):
    story.append(section_banner("Improvement trajectory", "Per-pool trend read, improver tier, and estimated percentile band where the sample supports it."))
    story.append(Spacer(1, 8))
    ip = analysis.get("improvement_profile", {})
    pref = ip.get("preferred")
    pref_label = ip.get("preferred_time_control")
    if pref and pref_label:
        cls = pref.get("classification", {})
        series = pref.get("series", {})
        text = (
            f"Primary read: <b>{pref_label}</b> from {fmt_num(series.get('start_rating'))} to {fmt_num(series.get('latest_rating'))} "
            f"(net {series.get('net_gain', 0):+}). This rates as <b>{cls.get('tier', '—')}</b> with an estimated band of "
            f"<b>{cls.get('estimated_percentile_band', '—')}</b>."
        )
        story.append(p(text, CALLOUT))
    rows = [["Pool", "Start", "Latest", "Net", "Tier", "Percentile band", "Fit"]]
    for label in ["bullet", "blitz", "rapid", "classical"]:
        entry = ip.get("by_time_control", {}).get(label)
        if entry:
            rows.append(improvement_row(label, entry))
    if len(rows) > 1:
        story.append(table(rows, [0.72 * inch, 0.58 * inch, 0.58 * inch, 0.48 * inch, 1.45 * inch, 1.9 * inch, 0.45 * inch]))
    else:
        story.append(p("No time-control-specific trend sample available.", BODY_LEFT))
    caveat = pref.get("classification", {}).get("caveat") if pref else None
    if caveat:
        story.append(Spacer(1, 5))
        story.append(p(caveat, SMALL))


def top_strengths(analysis: dict[str, Any]) -> list[str]:
    lines = []
    best_tc = best_pool_label(analysis.get("tc_performance", {}))
    if best_tc != "—":
        lines.append(f"Best practical pool: {best_tc}.")
    white_best_name, white_best = top_family(analysis.get("eco_white", {}), reverse=True)
    if white_best_name and white_best:
        lines.append(f"Best established White family: {white_best_name} at {white_best.get('score', 0):.1f}% ({white_best.get('games', 0)} games).")
    black_best_name, black_best = top_family(analysis.get("eco_black", {}), reverse=True)
    if black_best_name and black_best:
        lines.append(f"Best established Black family: {black_best_name} at {black_best.get('score', 0):.1f}% ({black_best.get('games', 0)} games).")
    pref = analysis.get("improvement_profile", {}).get("preferred")
    pref_label = analysis.get("improvement_profile", {}).get("preferred_time_control")
    if pref and pref_label:
        lines.append(f"Trend signal: {pref.get('classification', {}).get('tier', '—')} in {pref_label}.")
    if analysis.get("platform") == "lichess":
        rated = analysis.get("rated_performance")
        if rated:
            lines.append(f"Rated performance is healthy at {rated.get('score', 0):.1f}%.")
    return lines[:5]


def top_weaknesses(analysis: dict[str, Any]) -> list[str]:
    lines = []
    weakest_tc = weakest_pool_label(analysis.get("tc_performance", {}))
    if weakest_tc != "—":
        lines.append(f"Weakest main pool: {weakest_tc}.")
    white_worst_name, white_worst = top_family(analysis.get("eco_white", {}), reverse=False)
    if white_worst_name and white_worst:
        lines.append(f"White opening problem area: {white_worst_name} at {white_worst.get('score', 0):.1f}% ({white_worst.get('games', 0)} games).")
    black_worst_name, black_worst = top_family(analysis.get("eco_black", {}), reverse=False)
    if black_worst_name and black_worst:
        lines.append(f"Black opening problem area: {black_worst_name} at {black_worst.get('score', 0):.1f}% ({black_worst.get('games', 0)} games).")
    loss_by = analysis.get("loss_by", {})
    if loss_by:
        mode, count = max(loss_by.items(), key=lambda kv: kv[1])
        lines.append(f"Most common loss mode: {mode} ({count}).")
    pref = analysis.get("improvement_profile", {}).get("preferred")
    if pref and pref.get("classification", {}).get("tier") == "plateau / below-average improver":
        lines.append("Primary improvement trend is flat or negative in the main sample.")
    return lines[:5]


def practical_plan(analysis: dict[str, Any]) -> list[str]:
    lines = []
    weakest_tc = weakest_pool_label(analysis.get("tc_performance", {}))
    if weakest_tc != "—":
        lines.append(f"If format choice is available, push toward {weakest_tc.split(' ')[0]}.")
    white_worst_name, _ = top_family(analysis.get("eco_white", {}), reverse=False)
    if white_worst_name:
        lines.append(f"As Black, aim for {white_worst_name}-type positions if that fits your repertoire.")
    black_worst_name, _ = top_family(analysis.get("eco_black", {}), reverse=False)
    if black_worst_name:
        lines.append(f"As White, test their Black side in {black_worst_name} structures if your repertoire allows it.")
    loss_by = analysis.get("loss_by", {})
    if loss_by and loss_by.get("time", 0) >= max(loss_by.values()) / 2:
        lines.append("Keep the clock under pressure; time losses are a real share of the profile.")
    if analysis.get("platform") == "lichess" and analysis.get("vs_bots", {}).get("games", 0) > 0.1 * analysis.get("total", 1):
        lines.append("Adjust for bot-heavy sample bias when deciding how much to trust engine-like strategic habits.")
    return lines[:5]


def build_strengths_and_plan(story, analysis: dict[str, Any]):
    story.append(section_banner("Strengths and liabilities", "What should be respected, and what should be attacked."))
    story.append(Spacer(1, 8))
    split = Table([
        [Paragraph("Strengths", H2), Paragraph("Vulnerabilities", H2)],
        [bullet_block(top_strengths(analysis)), bullet_block(top_weaknesses(analysis))],
    ], colWidths=[3.2 * inch, 3.2 * inch])
    split.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(split)
    story.append(Spacer(1, 8))
    story.append(section_banner("Practical preparation plan", "Concrete matchup advice you can actually use over the board or online."))
    story.append(Spacer(1, 8))
    story.append(bullet_block(practical_plan(analysis)))


def build_appendix(story, analysis: dict[str, Any]):
    story.append(PageBreak())
    story.append(section_banner("Appendix", "Reference tables for opening families, rating bands, and frequent opponents."))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Opening families — White", H2))
    rows = [["Family", "Games", "Score", "W", "D", "L"]]
    for name, stats in sorted(analysis.get("eco_white", {}).items(), key=lambda kv: kv[1].get("games", 0), reverse=True)[:15]:
        rows.append([name, fmt_num(stats.get("games")), fmt_pct(stats.get("score")), fmt_num(stats.get("win")), fmt_num(stats.get("draw")), fmt_num(stats.get("loss"))])
    story.append(table(rows, [2.95 * inch, 0.58 * inch, 0.72 * inch, 0.45 * inch, 0.45 * inch, 0.45 * inch]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Opening families — Black", H2))
    rows = [["Family", "Games", "Score", "W", "D", "L"]]
    for name, stats in sorted(analysis.get("eco_black", {}).items(), key=lambda kv: kv[1].get("games", 0), reverse=True)[:15]:
        rows.append([name, fmt_num(stats.get("games")), fmt_pct(stats.get("score")), fmt_num(stats.get("win")), fmt_num(stats.get("draw")), fmt_num(stats.get("loss"))])
    story.append(table(rows, [2.95 * inch, 0.58 * inch, 0.72 * inch, 0.45 * inch, 0.45 * inch, 0.45 * inch]))

    bands = analysis.get("vs_rating_bands", {})
    if bands:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Results by opponent rating band", H2))
        rows = [["Band", "Games", "Score", "W", "D", "L"]]
        for name, stats in bands.items():
            rows.append([name, fmt_num(stats.get("games")), fmt_pct(stats.get("score")), fmt_num(stats.get("win")), fmt_num(stats.get("draw")), fmt_num(stats.get("loss"))])
        story.append(table(rows, [1.35 * inch, 0.58 * inch, 0.72 * inch, 0.45 * inch, 0.45 * inch, 0.45 * inch]))

    top_opp = analysis.get("top_opponents", [])
    if top_opp:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Most frequent opponents", H2))
        rows = [["Opponent", "Games", "Win", "Draw", "Loss"]]
        for row in top_opp[:10]:
            rows.append([row.get("name", "—"), fmt_num(row.get("games")), fmt_num(row.get("win")), fmt_num(row.get("draw")), fmt_num(row.get("loss"))])
        story.append(table(rows, [3.0 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch]))


def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, doc.pagesize[1] - 0.45 * inch, doc.pagesize[0] - doc.rightMargin, doc.pagesize[1] - 0.45 * inch)
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(doc.leftMargin, doc.pagesize[1] - 0.38 * inch, "OpenClaw · Chess Scout")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.line(doc.leftMargin, 0.52 * inch, doc.pagesize[0] - doc.rightMargin, 0.52 * inch)
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(analysis_path: Path, output_path: Path):
    analysis = json.loads(analysis_path.read_text())
    username = analysis.get("username", output_path.stem)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.62 * inch,
        title=f"Scouting Report — {username}",
        author="OpenClaw chess-opponent-scout",
        subject="Chess scouting dossier",
    )

    story = []
    build_cover(story, analysis_path, analysis)
    build_profile_snapshot(story, analysis)
    build_repertoire(story, analysis)
    build_style_and_time_controls(story, analysis)
    build_improvement(story, analysis)
    build_strengths_and_plan(story, analysis)
    build_appendix(story, analysis)

    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build_pdf.py <analysis.json> [output.pdf]")
        sys.exit(1)

    analysis_path = Path(sys.argv[1]).resolve()
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2]).resolve()
    else:
        output_path = analysis_path.with_name(f"{analysis_path.parent.name}-scouting-report.pdf")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(build_pdf(analysis_path, output_path))
