from pathlib import Path

import pytest

from src.main import Node, expand_node, expand_start_node, corner_handler, uppercase_handler, load_map_from_file, \
    load_nodes

compact_node_map = {
    (1, 0): Node(value='+', pos_x=1, pos_y=0), (2, 0): Node(value='-', pos_x=2, pos_y=0),
    (3, 0): Node(value='L', pos_x=3, pos_y=0), (4, 0): Node(value='-', pos_x=4, pos_y=0),
    (5, 0): Node(value='+', pos_x=5, pos_y=0), (1, 2): Node(value='B', pos_x=1, pos_y=2),
    (1, 1): Node(value='|', pos_x=1, pos_y=1), (4, 1): Node(value='+', pos_x=4, pos_y=1),
    (5, 1): Node(value='A', pos_x=5, pos_y=1), (6, 1): Node(value='-', pos_x=6, pos_y=1),
    (7, 1): Node(value='+', pos_x=7, pos_y=1), (0, 2): Node(value='@', pos_x=0,pos_y=2),
    (2, 2): Node(value='+', pos_x=2, pos_y=2), (4, 2): Node(value='+', pos_x=4, pos_y=2),
    (5, 2): Node(value='+', pos_x=5, pos_y=2), (7, 2): Node(value='H', pos_x=7, pos_y=2),
    (1, 3): Node(value='+', pos_x=1, pos_y=3), (2, 3): Node(value='+', pos_x=2, pos_y=3),
    (7, 3): Node(value='x', pos_x=7, pos_y=3)
}


def test_node_expansion():
    node_map = {
        (2, 2): Node(pos_x=2, pos_y=2, value='A'),
        (2, 3): Node(pos_x=2, pos_y=3, value='+'),
        (1, 2): Node(pos_x=1, pos_y=2, value='+'),
        (2, 1): Node(pos_x=2, pos_y=1, value='|'),
        (3, 2): Node(pos_x=3, pos_y=2, value='-'),
    }
    current_node = Node(pos_x=2, pos_y=2, value='A')
    previous_node = Node(pos_x=2, pos_y=1, value='|')
    neighbors = expand_node(previous_node=previous_node, current_node=current_node, nodes=node_map)
    assert len(neighbors) == 3


def test_start_node_expansion():
    node_map = {
        (2, 2): Node(pos_x=2, pos_y=2, value='A'),
        (2, 3): Node(pos_x=2, pos_y=3, value='+'),
        (1, 2): Node(pos_x=1, pos_y=2, value='+'),
        (2, 1): Node(pos_x=2, pos_y=1, value='|'),
        (3, 2): Node(pos_x=3, pos_y=2, value='-'),
        (2, 0): Node(pos_x=2, pos_y=0, value='-'),
    }
    current_node = Node(pos_x=2, pos_y=0, value='@')
    next_node = expand_start_node(start_node=current_node, nodes=node_map)
    assert next_node.pos_x == 2
    assert next_node.pos_y == 1
    assert next_node.value == '|'


def test_handle_corner_value():
    current_node = Node(value='+', pos_x=2, pos_y=2)
    previous_node = Node(value='B', pos_x=1, pos_y=2)
    neighbours = expand_node(previous_node=previous_node, current_node=current_node, nodes=compact_node_map)
    new_node, direction = corner_handler(current_node=current_node, neighbours=neighbours, direction=(1, 0))
    assert new_node.pos_x == 2 and new_node.pos_y == 3 and new_node.value == '+'
    assert direction[0] == 0 and direction[1] == 1


def test_handle_corner_value_error():
    # We'll set up the situation so that the path is going in the opposite direction than what should go to check this
    current_node = Node(value='A', pos_x=5, pos_y=1)
    previous_node = Node(value='+', pos_x=5, pos_y=0)
    neighbours = expand_node(previous_node=previous_node, current_node=current_node, nodes=compact_node_map)
    with pytest.raises(ValueError) as err:
        _ = corner_handler(current_node=current_node, neighbours=neighbours, direction=(-1, 0))
    assert "Fork" in str(err.value)


def test_uppercase_handler():
    previous_node = Node(value='+', pos_x=1, pos_y=3)
    current_node = Node(value='B', pos_x=1, pos_y=2)
    neighbours = expand_node(previous_node=previous_node, current_node=current_node, nodes=compact_node_map)
    new_node, direction = uppercase_handler(current_node=current_node, neighbours=neighbours, direction=(0, -1),
                                            nodes=compact_node_map)
    assert new_node.pos_x == 1 and new_node.pos_y == 1 and new_node.value == '|'
    assert direction[0] == 0 and direction[1] == -1


def test_dash_handler():
    current_node = Node(value='|', pos_x=1, pos_y=1)
    previous_node = Node(value='B', pos_x=1, pos_y=2)
    neighbours = expand_node(previous_node=previous_node, current_node=current_node, nodes=compact_node_map)
    new_node, direction = uppercase_handler(current_node=current_node, neighbours=neighbours, direction=(0, -1),
                                            nodes=compact_node_map)
    assert new_node.pos_x == 1 and new_node.pos_y == 0 and new_node.value == '+'
    assert direction[0] == 0 and direction[1] == -1


def test_load_map():
    map_str = load_map_from_file(Path('maps/load_map_test.txt'))
    assert len(map_str) == 1
    assert map_str[0] == '@ABCx'
    start_node, nodes = load_nodes(str_map=map_str)
    assert len(nodes) == 5
    assert start_node.pos_x == 0 and start_node.pos_y == 0
