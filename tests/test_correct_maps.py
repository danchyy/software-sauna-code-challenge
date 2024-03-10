import pytest

from src.main import main


def test_basic():
    letters, path = main('maps/basic.txt')
    assert letters == "ACB"
    assert path == "@---A---+|C|+---+|+-B-x"


def test_compact():
    letters, path = main('maps/compact.txt')
    assert letters == "BLAH"
    assert path == "@B+++B|+-L-+A+++A-+Hx"


def test_compact_2():
    letters, path = main('maps/compact_2.txt')
    assert letters == "FOO"
    assert path == "@++-F+++F|+--O+-O+++O||x"


def test_goonies():
    letters, path = main('maps/goonies.txt')
    assert letters == "GOONIES"
    assert path == "@-G-O-+|+-+|O||+-O-N-+|I|+-+|+-I-+|ES|x"


def test_ignore_after_end():
    letters, path = main('maps/ignore_after_end.txt')
    assert letters == "AB"
    assert path == "@-A--+|+-B--x"


def test_intersection():
    letters, path = main('maps/intersection.txt')
    assert letters == "ABCD"
    assert path == "@|A+---B--+|+--C-+|-||+---D--+|x"


def test_letter_turns():
    letters, path = main('maps/letter_turns.txt')
    assert letters == "ACB"
    assert path == "@---A---+|||C---+|+-B-x"


def test_letter_only():
    letters, path = main('maps/letter_only.txt')
    assert letters == "ABCDEFGHIJKLMNOPQR"
    assert path == "@ABCDEFGHIJKLMNOPQNRx"


def test_snake():
    letters, path = main('maps/snake.txt')
    assert letters == "SNAKE"
    assert path == "@--S--+|+-----N|+-----A-----+|||K-----E|||x"


def test_goofy():
    letters, path = main('maps/goofy.txt')
    assert letters == "GOOFY"
    assert path == "@-++-++-++-++-G-+|+-+|O+|+-O+++O|+-------F|Yx"


def test_spiral():
    letters, path = main('maps/spiral.txt')
    assert letters == "SPIRAL"
    assert path == "@S----P||I-----RA--L++x"


def test_tough_corner():
    letters, path = main('maps/tough_corner.txt')
    assert letters == "A"
    assert path == "@A---+|+--+||+---++--+x"

def test_dummy():
    letters, path = main('maps/dummy.txt')
    assert letters == "DUMMY"
    assert path == "@D---+|U+++U-----+MM++-Y-x"