from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Sequence, Optional
from argparse import ArgumentParser


_START_CHAR = '@'
_END_CHAR = 'x'
_HORIZONTAL_DIRECTION = '-'
_VERTICAL_DIRECTION = '|'
_CORNER = '+'
SPECIAL_CHARS = [_START_CHAR, _END_CHAR, _HORIZONTAL_DIRECTION, _VERTICAL_DIRECTION, _CORNER]


@dataclass
class Node:
    value: str
    pos_x: int
    pos_y: int


def load_map_from_file(file_path: Path) -> List[str]:
    """
    Loads map layout from file in form of list of strings
    :param file_path: Path to the target file
    :return: List of strings
    """
    with file_path.open() as f:
        return [line.strip('\n') for line in f.readlines()]


def load_nodes(str_map: List[str]) -> Tuple[Node, Dict[Tuple[int, int], Node]]:
    """
    Parses string map into a dictionary of positions and non-empty nodes. Along with that, it finds a starting node
    that is marked with character @ and returns it directly.

    :param str_map: Map to be parsed
    :return: Starting Node and all other nodes
    """
    node_dict = {}
    start_node = None
    end_node_found = False
    for i in range(len(str_map)):
        for j in range(len(str_map[i])):
            if str_map[i][j] == _START_CHAR:
                if start_node is not None:
                    raise ValueError("Multiple start characters")
                start_node = Node(value=str_map[i][j], pos_x=j, pos_y=i)
                continue
            elif str_map[i][j] == _END_CHAR:
                end_node_found = True
            node_dict[(j, i)] = Node(value=str_map[i][j], pos_x=j, pos_y=i)

    if start_node is None:
        raise ValueError("Missing start character")
    if end_node_found is False:
        raise ValueError("Missing end character")
    return start_node, node_dict


def expand_node(
        previous_node: Node,
        current_node: Node,
        nodes: Dict[Tuple[int, int], Node]
) -> List[Node]:
    pos_x, pos_y = current_node.pos_x, current_node.pos_y
    neighbours = [nodes.get((pos_x - 1, pos_y), None), nodes.get((pos_x + 1, pos_y), None),
                  nodes.get((pos_x, pos_y - 1), None), nodes.get((pos_x, pos_y + 1), None)]
    return [n for n in neighbours if n is not None and n.value != ' ' and not (n.pos_y == previous_node.pos_y
            and n.pos_x == previous_node.pos_x)]


def expand_start_node(start_node: Node, nodes: Dict[Tuple[int, int], Node]) -> Node:
    start_neighbours = expand_node(current_node=start_node, nodes=nodes, previous_node=start_node)
    if len(start_neighbours) == 0:
        raise ValueError("No neighbours for starting point")
    if len(start_neighbours) > 1:
        raise ValueError("Multiple starting paths")
    return start_neighbours[0]


def handle_same_direction(
        current_node: Node,
        nodes: Dict[Tuple[int, int], Node],
        direction: Tuple[int, int]
) -> Optional[Node]:
    next_position = (current_node.pos_x + direction[0], current_node.pos_y + direction[1])
    current_node = nodes.get(next_position, None)
    return current_node


def handle_uppercase(
        current_node: Node,
        nodes: Dict[Tuple[int, int], Node],
        neighbours: List[Node],
        direction: Tuple[int, int]
) -> Tuple[Node, Tuple[int, int]]:
    if len(neighbours) > 1:
        # keep direction if crossroad
        next_position = (current_node.pos_x + direction[0], current_node.pos_y + direction[1])
        return nodes.get(next_position, None), direction
    return neighbours[0], (neighbours[0].pos_x - current_node.pos_x, neighbours[0].pos_y - current_node.pos_y)


def handle_corner(
        current_node: Node,
        neighbours: List[Node],
        direction: Tuple[int, int]
) -> Tuple[Node, Tuple[int, int]]:
    f_n = [
        n for n in neighbours if not (
                n.pos_x - current_node.pos_x == direction[0] and n.pos_y - current_node.pos_y == direction[1])
    ]
    if len(f_n) > 1:
        raise ValueError("Fork in path")
    if len(f_n) == 0:
        raise ValueError("Fake turn")
    return f_n[0], (f_n[0].pos_x - current_node.pos_x, f_n[0].pos_y - current_node.pos_y)


def traverse(start_node: Node, nodes: Dict[Tuple[int, int], Node]) -> Sequence[Node]:
    visited = [start_node]
    current_node = expand_start_node(start_node, nodes)
    direction = (current_node.pos_x - start_node.pos_x, current_node.pos_y - start_node.pos_y)
    while True:
        if current_node is None:
            raise ValueError("Node can't be None", visited)
        neighbours = expand_node(current_node=current_node, previous_node=visited[-1], nodes=nodes)
        if current_node == visited[-1]:
            break
        visited.append(current_node)
        if current_node.value == _END_CHAR:
            return visited
        if len(neighbours) == 0:
            raise ValueError("Broken path")
        if current_node.value.isupper():
            current_node, direction = handle_uppercase(
                current_node=current_node,
                nodes=nodes,
                neighbours=neighbours,
                direction=direction
            )
        else:
            if current_node.value == _CORNER:
                current_node, direction = handle_corner(
                    current_node=current_node,
                    neighbours=neighbours,
                    direction=direction
                )
            else:
                current_node = handle_same_direction(current_node=current_node, direction=direction, nodes=nodes)
                if current_node is None:
                    raise ValueError("Invalid Corner")


def main(file_path: str) -> Tuple[str, str]:
    start_node, node_map = load_nodes(load_map_from_file(Path(file_path)))
    nodes = traverse(start_node=start_node, nodes=node_map)
    visited_letter_nodes = set()
    visited_letters = []
    full_path = []
    for node in nodes:
        if node.value.isupper() and (node.pos_x, node.pos_y) not in visited_letter_nodes:
            visited_letters.append(node.value)
            visited_letter_nodes.add((node.pos_x, node.pos_y))
        full_path.append(node.value)
    print("".join(visited_letters))
    print("".join(full_path))
    return "".join(visited_letters), "".join(full_path)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='Path to the map')
    args = parser.parse_args()
    main(args.path)
