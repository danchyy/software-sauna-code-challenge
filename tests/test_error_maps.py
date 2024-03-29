import pytest

from src.main import main


def test_error_broken_path():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_broken_path.txt')
    assert "Broken path" in str(err.value)


def test_error_fake_turn():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_fake_turn.txt')
    assert "Fake turn" in str(err.value)


def test_error_fork():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_fork.txt')
    assert "Fork" in str(err.value)


def test_error_tough_fork():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_tough_fork.txt')
    assert "Fork" in str(err.value)


def test_error_missing_start():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_missing_start.txt')
    assert "Missing start" in str(err.value)


def test_error_missing_end():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_missing_end.txt')
    assert "Missing end" in str(err.value)


def test_error_multiple_start():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_multiple_starts.txt')
    assert "Multiple start characters" in str(err.value)


def test_error_multiple_start_2():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_multiple_starts_2.txt')
    assert "Multiple start characters" in str(err.value)


def test_error_multiple_start_3():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_multiple_starts_3.txt')
    assert "Multiple start characters" in str(err.value)


def test_error_multiple_start_neighbours():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_multiple_start_neighbours.txt')
    assert "Multiple starting paths" in str(err.value)


def test_error_err_invalid_uppercase_intersection():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_invalid_uppercase_intersection.txt')
    assert "3 surrounding chars" in str(err.value)


def test_error_invalid_char():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_invalid_char.txt')
    assert "Invalid char" in str(err.value)


def test_error_tough():
    with pytest.raises(ValueError) as err:
        main('maps/errors/err_tough.txt')
    assert "problematic node" in str(err.value)
