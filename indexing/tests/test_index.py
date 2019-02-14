from django.conf import settings
settings.configure()
import sys, os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from index_parser import IndexParser

def test_end2end():
    data = [
        'C',
        'Ccccccc, asdf',
        '- cccc',
        '-- ffffff',
        '--- hhhh',
        '--- gggg',
        '- bbbbb',
        '-- ddddd',
        '--- eeee',
        '-- cccc',
        '- aaaa',
        '-- bbbb',
        '-- aaaa',
        'B',
        '- z',
        '-- a',
        '- x',
        '- y',
        'A',
        'Aaaaaaaaa',
        '- zzz',
        '-- żżżżżż',
        '- xxx',
        '-- yyy',
    ]
    expected = [
        'A',
        'Aaaaaaaaa',
        '– xxx',
        '– – yyy',
        '– zzz',
        '– – żżżżżż',
        '',
        'B',
        '– x',
        '– y',
        '– z',
        '– – a',
        '',
        'C',
        'Ccccccc, asdf',
        '– aaaa',
        '– – aaaa',
        '– – bbbb',
        '– bbbbb',
        '– – cccc',
        '– – ddddd',
        '– – – eeee',
        '– cccc',
        '– – ffffff',
        '– – – gggg',
        '– – – hhhh',
    ]
    parser = IndexParser()
    parsed = parser.parse(data)
    assert parsed == expected

def test_alphabetical_order_ci():
    data = [
        'c',
        '– ż',
        '– Ą',
        'A',
        '– b',
        '– A',
        '– – a',
        '– – B',
        'B',
    ]
    expected = [
        'A',
        '– A',
        '– – a',
        '– – B',
        '– b',
        '',
        'B',
        '',
        'c',
        '– Ą',
        '– ż',
    ]
    parser = IndexParser()
    parsed = parser.parse(data)
    assert parsed == expected

def test_hyphens():
    data = [
        'A, do-not-change, 80-100',
        '- A, 01-02',
        '– - B, still-0',
        '– b, 1-2, 2-4, 5-6',
        'b',
        'Bb, 5-still',
    ]
    expected = [
        'A, do-not-change, 80–100',
        '– A, 01–02',
        '– – B, still-0',
        '– b, 1–2, 2–4, 5–6',
        '',
        'b',
        'Bb, 5-still',
    ]
    parser = IndexParser()
    parsed = parser.parse(data)
    print(parsed)
    assert parsed == expected
