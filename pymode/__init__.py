""" Pymode support functions. """

from __future__ import absolute_import

import sys
import vim  # noqa


def auto():
    """ Fix PEP8 erorrs in current buffer. """
    from .autopep8 import fix_code

    class Options(object):
        aggressive = int(vim.eval('g:pymode_autoPEP8_aggressive'))
        diff = False
        experimental = False
        ignore = vim.eval('g:pymode_lint_ignore')
        in_place = True
        indent_size = int(vim.eval('&tabstop'))
        line_range = None
        max_line_length = int(vim.eval('g:pymode_options_max_line_length'))
        pep8_passes = 100
        recursive = False
        select = vim.eval('g:pymode_lint_select')
        verbose = 0

    original = '\n'.join(vim.current.buffer[:])
    fixed = fix_code(original, Options)
    if not fixed:
        return 1
    if fixed == original:
        return
    vim.current.buffer[:] = fixed.split('\n')
    if vim.current.buffer[-1] == '':
        del vim.current.buffer[-1]


def get_documentation():
    """ Search documentation and append to current buffer. """
    from ._compat import StringIO

    sys.stdout, _ = StringIO(), sys.stdout
    help(vim.eval('a:word'))
    sys.stdout, out = _, sys.stdout.getvalue()
    vim.current.buffer.append(str(out).splitlines(), 0)
