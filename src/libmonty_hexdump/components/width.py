#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Width
"""

# imports: project
from libmonty_hexdump.components import lines


def determine_count_per_line(cols: int = 80,
                             full_width: bool = False
                             ) -> int:
    """Determine count per line"""

    if full_width:
        for count in range(1, cols):
            if min_line_length(count) > cols:
                return count - 1

    if cols < min_line_length(16):  # 78
        return 8

    if cols < min_line_length(24):  # 110
        return 16

    if cols < min_line_length(32):  # 142
        return 24

    return 32


def min_line_length(bytes_per_line: int) -> int:
    """Minimum line length"""

    line_length: int = len(lines.construct(bytes(bytes_per_line), bytes_per_line))
    line_end_character_offset: int = 1

    return line_length + line_end_character_offset
