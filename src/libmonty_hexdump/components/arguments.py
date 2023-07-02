#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Arguments
"""

# imports: library
from argparse import ArgumentParser
from typing import Callable, Union

# imports: dependencies
from libmonty.formatting import char_str, number_str

# imports: project
from libmonty_hexdump.components import streams


def create_arguments(parser_hexer: ArgumentParser) -> None:
    """Create arguments"""

    parser_hexer.add_argument('-s', '--stream',
                              help='Stream',
                              action='store', type=str, default='random',
                              dest='stream')

    parser_hexer.add_argument('-b', '--bytes-per-line',
                              help='Bytes per line',
                              action='store', type=int, default=16,
                              dest='bytes_per_line')

    parser_hexer.add_argument('-p', '--sleep',
                              help='Sleep time between lines',
                              action='store', type=float, default=0.01,
                              dest='sleep')

    parser_hexer.add_argument('-i', '--index-format',
                              help='Index format',
                              action='store', type=str, default='hexadecimal',
                              dest='index_format')


def stream(source: Union[Callable, str]) -> (Callable, Callable):
    """Stream source"""

    if isinstance(source, Callable):
        f_stream: Callable = source
        f_char_converter: Callable = char_str.byte_to_compact_printable_with_dots

    else:
        if source == 'random':
            f_stream: Callable = streams.random_data
            f_char_converter: Callable = char_str.byte_to_compact_printable_with_dots

        else:
            try:
                f_stream: Callable = streams.create_from_file(source)
            except FileNotFoundError as exc:
                raise ValueError(str(exc)) from exc

            f_char_converter: Callable = char_str.byte_to_compact_printable_with_frames

    return f_stream, f_char_converter


def bytes_per_line(count: int) -> int:
    """Bytes per line"""

    if count < 1:
        raise ValueError

    return count


def sleep(speed: Union[float, int, str]) -> float:
    """Sleep"""

    speeds: dict[str, float] = {
        'f': 0.01,
        'fast': 0.01,
        'm': 0.05,
        'med': 0.05,
        'medium': 0.05,
        's': 0.1,
        'slow': 0.1,
        'step': 0.5
    }

    if isinstance(speed, int):
        speed: float = float(speed)

    if isinstance(speed, (float, int)):
        if speed <= 0:
            raise ValueError

    elif isinstance(speed, str):
        try:
            speed: float = speeds[speed]
        except KeyError:
            print(f'Bad value for \'sleep\': \'{speed}\'')
            speed = 0.01
            print(f'Using default value for \'sleep\': \'{speed}\'')

    return speed


def index_converter(converter: Union[Callable, str]) -> Callable:
    """Index converter"""

    index_formats: dict[str, Callable] = {
        'h': number_str.hexadecimal,
        'hex': number_str.hexadecimal,
        'hexadecimal': number_str.hexadecimal,

        'd': number_str.decimal,
        'dec': number_str.decimal,
        'decimal': number_str.decimal,

        'o': number_str.octal,
        'oct': number_str.octal,
        'octal': number_str.octal
    }

    if isinstance(converter, Callable):
        return converter

    try:
        return index_formats[converter]
    except KeyError:
        print(f'Value for index format not recognized: \'{converter}\'')
        converter: str = 'hexadecimal'
        print(f'Using default value for index format: \'{converter}\'')
        return index_formats[converter]
