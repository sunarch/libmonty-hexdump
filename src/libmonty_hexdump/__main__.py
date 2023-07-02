#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""hexdump - main
"""

# imports: library
from argparse import ArgumentParser, Namespace
import time
from typing import Callable

# imports: dependencies
from libmonty.environment import terminal
from libmonty_logging.config.file_and_stream.v1 import config as logging_config
import libmonty_logging.helper as logging_helper
# import libmonty_logging.message as logging_message

# imports: project
from libmonty_hexdump import version
from libmonty_hexdump.components import arguments
from libmonty_hexdump.components import width
from libmonty_hexdump.components import lines


def main() -> None:
    """Main"""

    logging_helper.apply_config(version.PROGRAM_NAME,
                                version.__version__,
                                logging_config)

    # logging_message.program_header(version.PROGRAM_NAME)

    parser = ArgumentParser(prog=version.PROGRAM_NAME)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_true',
                        dest='version')

    arguments.create_arguments(parser)

    args: Namespace = parser.parse_args()

    if args.version:
        print(f'{version.PROGRAM_NAME} {version.__version__}')
        return

    main_lib(args)


def main_lib(args: Namespace) -> None:
    """Main lib"""

    try:
        stream, char_converter = arguments.stream(args.stream)
        bytes_per_line: int = arguments.bytes_per_line(args.bytes_per_line)
        sleep_seconds: float = arguments.sleep(args.sleep)
        index_converter: Callable = arguments.index_converter(args.index_format)
    except ValueError as exc:
        raise ValueError from exc

    try:
        run(stream, index_converter, char_converter, bytes_per_line, sleep_seconds)
    except ValueError as exc:
        raise ValueError from exc


def run(stream: Callable = None,
        index_converter: Callable = None,
        char_converter: Callable = None,
        bytes_per_line: int = 0,
        sleep_seconds: float = 0.1
        ) -> None:
    """Run"""

    if stream is None:
        raise ValueError('No input stream specified!')

    if index_converter is None:
        raise ValueError('No index formatting method specified!')

    if char_converter is None:
        raise ValueError('No char conversion method specified!')

    print('')

    extra_width: int = 0

    if bytes_per_line <= 0:
        column_count: int = terminal.get_cols()

        is_full_width: bool = False
        if bytes_per_line <= -1:
            is_full_width: bool = True

        bytes_per_line: int = width.determine_count_per_line(column_count, is_full_width)

        if is_full_width:
            extra_width: int = column_count - width.min_line_length(bytes_per_line)

    offset: int = 0

    lines.print_header(bytes_per_line, index_converter, extra_width)
    print('')

    for bytes_unit in stream(bytes_per_line):

        try:
            lines.print_data(bytes_unit,
                             bytes_per_line,
                             offset,
                             index_converter,
                             char_converter,
                             extra_width)
            time.sleep(sleep_seconds)

            offset += bytes_per_line

        except KeyboardInterrupt:
            break

    print('', flush=True)


if __name__ == '__main__':
    main()
