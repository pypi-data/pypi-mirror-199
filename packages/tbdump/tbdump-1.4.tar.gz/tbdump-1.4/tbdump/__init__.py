#!/usr/bin/env python3
#
# Display helpful information for debbugging in case of errors/exceptions.
# Copyright (c) 2018-2023, Hiroyuki Ohsaki.
# All rights reserved.
#

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import linecache
import pdb
import sys
import traceback

import ansiterm as at

MODULES_TO_HIDE = ['__builtins__']

def _print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

def trimmed_str(astr, ncols=60):
    """Trim the string ASTR to fit within NCOLS columns."""
    if len(astr) >= ncols:
        return astr[:ncols] + '...'
    else:
        return astr

def print_tb(tb, nlines=5, ncols=80):
    """Pretty print the traceback TB.  NLINES of Python source lines are
    displayed.  All output lines are fitted within NCOLS column."""
    f = tb.tb_frame
    lineno = tb.tb_lineno
    co = f.f_code
    filename = co.co_filename
    name = co.co_name

    # Display frame header.
    name_str = at.blue(name, True)
    filename_str = at.green(filename)
    _print('----', name_str, filename_str)

    # Display source lines.
    linecache.checkcache(filename)
    errline = ''
    for n in range(lineno - nlines + 1, lineno + 1):
        line = linecache.getline(filename, n, f.f_globals).rstrip()
        if line is not None:
            lineno_str = at.magenta('{:5} '.format(n))
            _print(lineno_str, end='')
            if n == lineno:
                line_str = at.red(line)
                errline = line
            else:
                line_str = at.reset(line)
            _print(line_str)

    def _by_location(key):
        pos = errline.find(key)
        if 0 <= pos <= 255:
            # Keys matching the error line come first.
            return chr(pos)
        elif key.startswith('__'):
            # Keys starting with __ come last.
            return '~' + key
        else:
            # Sorted in the alphabetical order.
            return key

    # Dump all local variables in the frame.
    keys = sorted(f.f_locals.keys(), key=_by_location)
    for key in keys:
        key_str = at.yellow('{:>20}'.format(key))
        if key in sys.modules or key in MODULES_TO_HIDE:
            _print(key_str, '= ...')
            continue
        else:
            val_str = trimmed_str(repr(f.f_locals[key]), ncols - 20)
            _print(key_str, '=', val_str)

        # Dump all attributes for objects.
        attr = getattr(f.f_locals[key], '__dict__', None)
        if attr:
            keys = sorted(attr.keys(), key=_by_location)
            for key in keys:
                key_str = at.cyan('{:>28}'.format(key))
                val_str = trimmed_str(repr(attr[key]), ncols - 28)
                _print(key_str, val_str)

def print_exc(etype, value, tb):
    """Exception handler based on the code in O'Reilly's Python cookbook.
    This function receives the same arguments with traceback.print_exc: i.e.,
    exception type ETYA, exception value VALUE, and traceback object TB."""
    if issubclass(etype, SyntaxError):
        sys.__excepthook__(etype, value, tb)
    elif issubclass(etype, BrokenPipeError):
        sys.__excepthook__(etype, value, tb)
    else:
        # Dump all frames.
        while True:
            print_tb(tb)
            tb = tb.tb_next
            if not tb:
                break

        # Display info on exception.
        lines = traceback.format_exception_only(etype, value)
        for line in lines:
            _print(at.red(line))

        # Invoke debugger if possible.
        if sys.stderr.isatty() and sys.stdin.isatty():
            pdb.pm()

# Override the exception hook.
sys.excepthook = print_exc

def main():
    # Intentionally raise NameError.
    print(x)

if __name__ == "__main__":
    main()
