#!/usr/bin/env python3
"""Shared IO/output helpers for opening guide generators."""

from __future__ import annotations

import json

import weasyprint


def load_guide_data(input_json):
    with open(input_json) as f:
        return json.load(f)


def write_guide_outputs(html, html_debug, output_path, summary_line=None):
    with open(html_debug, 'w') as f:
        f.write(html)
    weasyprint.HTML(string=html).write_pdf(str(output_path))
    print(f'PDF generated: {output_path}')
    if summary_line:
        print(summary_line)

