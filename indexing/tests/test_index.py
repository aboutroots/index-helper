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