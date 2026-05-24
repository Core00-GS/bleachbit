#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2008-2026 Andrew Ziem.
#
# This work is licensed under the terms of the GNU GPL, version 3 or
# later.  See the COPYING file in the top-level directory.
"""Normalize .pot/.po files for gettext on Windows.

xgettext on Windows may emit backslashes in #: lines and CRLF line endings;
forward slashes and Unix (LF) newlines keep diffs stable and avoid msgmerge
producing invalid reference continuations when inputs are mixed LF/CRLF.
"""

from __future__ import print_function

import argparse
import sys


def normalize_po(path):
    with open(path, 'rb') as handle:
        text = handle.read().decode('utf-8')
    lines = text.splitlines()
    with open(path, 'w', encoding='utf-8', newline='\n') as handle:
        for line in lines:
            if line.startswith('#:'):
                line = line.replace('\\', '/')
            handle.write(line + '\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pofile', help='Path to the .pot or .po file to update in place')
    args = parser.parse_args(argv)
    try:
        normalize_po(args.pofile)
    except IOError as err:
        print('error: %s' % err, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
