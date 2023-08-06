""" Test counts
"""

from pathlib import Path

import nbwc

HERE = Path(__file__).parent


def test_counts():
    for fn in HERE.glob('eg_nb.*'):
        assert nbwc.wc_nb(fn) == 24
        assert nbwc.wc_nb(fn, types=('raw',)) == 16
        assert nbwc.wc_nb(fn, types=('code',)) == 18
        assert nbwc.wc_nb(fn, types=('markdown', 'raw',)) == 40
        assert nbwc.wc_nb(fn, types=('markdown', 'raw', 'code')) == 58
