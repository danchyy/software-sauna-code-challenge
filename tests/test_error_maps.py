import pytest

from src.main import main


def test_error_broken_path():
    with pytest.raises(ValueError) as err:
        main('maps/err_broken_path.txt')
    assert "Broken path" in str(err.value)

def test_error_fake_turn():
    with pytest.raises(ValueError) as err:
        main('maps/err_fake_turn.txt')
    assert "Fake turn" in str(err.value)


def test_error_fork():
    with pytest.raises(ValueError) as err:
        main('maps/err_fork.txt')
    assert "Fork" in str(err.value)


def test_error_missing_start():
    with pytest.raises(ValueError) as err:
        main('maps/err_missing_start.txt')
    assert "Missing start" in str(err.value)


def test_error_missing_end():
    with pytest.raises(ValueError) as err:
        main('maps/err_missing_end.txt')
    assert "Missing end" in str(err.value)


def test_error_multiple_start():
    with pytest.raises(ValueError) as err:
        main('maps/err_multiple_starts.txt')
    assert "Multiple start characters" in str(err.value)


def test_error_multiple_start_2():
    with pytest.raises(ValueError) as err:
        main('maps/err_multiple_starts_2.txt')
    assert "Multiple start characters" in str(err.value)


def test_error_multiple_start_3():
    with pytest.raises(ValueError) as err:
        main('maps/err_multiple_starts_3.txt')
    assert "Multiple start characters" in str(err.value)


def test_error_multiple_start_neighbours():
    with pytest.raises(ValueError) as err:
        main('maps/err_multiple_start_neighbours.txt')
    assert "Multiple starting paths" in str(err.value)