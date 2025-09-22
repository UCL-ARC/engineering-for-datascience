from ..gather import *

import pytest
import os

def test_can_parse_index():
    with open(os.path.join(os.path.dirname(__file__),
        'fixtures',
        'index.html')) as fixture_file:
        result = list(parse_index(fixture_file))
        assert len(result)==13
        assert result[0]=="https://bl.iro.bl.uk/concern/datasets/e0e7b9c8-1d83-4275-afa4-51b255d695a3?locale=en"

def test_can_parse_cover():
    with open(os.path.join(os.path.dirname(__file__),
        'fixtures',
        'cover_page.html')) as fixture_file:
        assert parse_cover_page(fixture_file) == "https://bl.iro.bl.uk/downloads/135c0882-1e09-4d0a-8d88-a8ac41066b10?locale=en"
