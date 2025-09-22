from ..combine import *

import pytest
import os

def test_can_analyse_results():
    fixture = os.path.join(os.path.dirname(__file__),
        'fixtures','results')
    result = combiner(fixture)
    assert result["1960"] == 10
    assert result["1970"] == 13
    assert result["1980"] == 11