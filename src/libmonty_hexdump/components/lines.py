#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Lines
"""

# imports: library
from typing import Callable

# imports: dependencies
from libmonty.formatting import number_str
from libmonty.formatting import char_str


COUNTER_DIGITS = 10


def print_header(bytes_per_line: int,
                 index_converter: Callable,
                 extra_width: int
                 ) -> None:
    """Print header"""

    counter_text: str = f'Offset ({index_converter(-1)})'
    line: str = f' {counter_text:^{COUNTER_DIGITS + extra_width}}  '

    try:
        bytes_unit: bytes = bytes(range(bytes_per_line))
    except ValueError:
        if bytes_per_line > 256:
            full: bytes = bytes(range(256)) * (bytes_per_line // 256)
            fraction: bytes = bytes(range(bytes_per_line % 256))
            bytes_unit: bytes = full + fraction
        else:
            raise

    line += _part_bytes(bytes_unit, bytes_per_line, index_converter)

    line += 'Decoded text'

    print(line, flush=True)


def print_data(b_unit: bytes,
               bytes_per_line: int,
               offset: int,
               index_converter: Callable,
               char_converter: Callable,
               extra_width: int
               ) -> None:
    """Print data"""

    text: str = construct(
        b_unit,
        bytes_per_line,
        offset,
        index_converter,
        char_converter,
        extra_width
    )

    print(text, flush=True)


def construct(b_unit: bytes,
              bytes_per_line: int,
              offset: int = 0,
              index_converter: Callable = number_str.pseudo,
              char_converter: Callable = char_str.pseudo,
              extra_width: int = 0
              ) -> str:
    """Construct"""

    counter_text: str = _part_counter(offset, COUNTER_DIGITS + extra_width, index_converter)

    bytes_text: str = _part_bytes(b_unit, bytes_per_line, number_str.hexadecimal)

    chars_text: str = _part_chars(b_unit, char_converter)

    return counter_text + bytes_text + chars_text


def _part_counter(offset: int = 0,
                  digits: int = COUNTER_DIGITS,
                  index_formatter: Callable = number_str.pseudo,
                  ) -> str:
    """Part: counter"""

    return ' ' + index_formatter(offset, digits) + '  '


def _part_bytes(b_unit: bytes,
                bytes_per_line: int,
                number_converter: Callable = number_str.pseudo
                ) -> str:
    """Part: bytes"""

    bytes_text: str = ' '.join(map(lambda b: number_converter(b, 2), b_unit))

    if len(b_unit) < bytes_per_line:
        format_string: str = '{:<' + str((bytes_per_line * 3) - 1) + '}'
        bytes_text: str = format_string.format(bytes_text)

    return bytes_text + '  '


def _part_chars(bytes_unit: bytes,
                char_converter: Callable = char_str.pseudo,
                ) -> str:
    """Part: chars"""

    return ''.join(map(char_converter, bytes_unit))
