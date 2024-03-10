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
            if str_map[i][j] == ' ':
                continue
            node_dict[(j, i)] = Node(value=str_map[i][j], pos_x=j, pos_y=i)
            if str_map[i][j] == _START_CHAR:
                if start_node is not None:
                    raise ValueError("Multiple start characters")
                start_node = Node(value=str_map[i][j], pos_x=j, pos_y=i)
                continue
            elif str_map[i][j] == _END_CHAR:
                end_node_found = True

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
    """
    Collects all of the nodes except the previous ones as we never want to turn around (180 degrees) and return. This
    sort of mechanism avoids the use of "visited" list other than to keep track of our path.

    :param previous_node: Previously visited node
    :param current_node: Current node
    :param nodes: Entire map of nodes
    :return: Neighbouring nodes
    """
    pos_x, pos_y = current_node.pos_x, current_node.pos_y
    neighbours = [nodes.get((pos_x - 1, pos_y), None), nodes.get((pos_x + 1, pos_y), None),
                  nodes.get((pos_x, pos_y - 1), None), nodes.get((pos_x, pos_y + 1), None)]
    return [n for n in neighbours if n is not None and n.value != ' ' and not (n.pos_y == previous_node.pos_y
            and n.pos_x == previous_node.pos_x)]


def expand_start_node(start_node: Node, nodes: Dict[Tuple[int, int], Node]) -> Node:
    """
    Same as `expand_node` but just for the start case as it has some extra error handling.

    :param start_node: Start node
    :param nodes: Entire map of nodes
    :return: Neighbouring nodes
    """
    start_neighbours = expand_node(current_node=start_node, nodes=nodes, previous_node=start_node)
    if len(start_neighbours) == 0:
        raise ValueError("No neighbours for starting point")
    if len(start_neighbours) > 1:
        raise ValueError("Multiple starting paths")
    return start_neighbours[0]


def dash_handler(
        current_node: Node,
        nodes: Dict[Tuple[int, int], Node],
        direction: Tuple[int, int]
) -> Optional[Node]:
    """
    Handler which just takes the existing direction and returns the next node in that direction (left, right, up
    or down). Returns None if there is no node at that position (which later throws an error).

    :param current_node: Current Node
    :param nodes: All Nodes on the map
    :param direction: Direction of the path
    :return: Next node or None
    """
    next_position = (current_node.pos_x + direction[0], current_node.pos_y + direction[1])
    current_node = nodes.get(next_position, None)
    return current_node


def uppercase_handler(
        current_node: Node,
        nodes: Dict[Tuple[int, int], Node],
        neighbours: List[Node],
        direction: Tuple[int, int]
) -> Tuple[Node, Tuple[int, int]]:
    """
    Handler which takes care of uppercase letter, it determines if we've reached an intersection - then takes the node
    that follows the direction. If that's not the case then the letter should have only one neighbor and path should
    continue with that node and direction.
    :param current_node: Current node
    :param nodes: All nodes on map
    :param neighbours: Neighbouring nodes
    :param direction: Direction of the path
    :return: Next node and new direction
    """
    # TODO add more error handling - when len(neighbours) == 2 - that's an error
    if len(neighbours) == 2:
        raise ValueError("Found letter intersection with 3 surrounding chars - don't know what to do!")
    if len(neighbours) == 3:
        # keep direction if crossroad
        next_position = (current_node.pos_x + direction[0], current_node.pos_y + direction[1])
        return nodes.get(next_position, None), direction
    if len(neighbours) == 0:
        raise ValueError("End of path - invalid map")
    return neighbours[0], (neighbours[0].pos_x - current_node.pos_x, neighbours[0].pos_y - current_node.pos_y)


def corner_handler(
        current_node: Node,
        neighbours: List[Node],
        direction: Tuple[int, int]
) -> Tuple[Node, Tuple[int, int]]:
    """
    Performs a turn by 90 degrees, if that's not possible it throws an error.

    :param current_node: Current node
    :param neighbours: Neighbouring nodes
    :param direction: Direction of the path
    :return: Next node and new direction
    """
    f_n = [
        n for n in neighbours if not (
                n.pos_x - current_node.pos_x == direction[0] and n.pos_y - current_node.pos_y == direction[1])
    ]
    if len(f_n) > 1:
        # Check potential Fork
        valid_n = []
        for n in f_n:
            # Check if corner neighbour nodes are valid -> they can either continue direction or turn right away
            candidate_direction = (n.pos_x - current_node.pos_x, n.pos_y - current_node.pos_y)
            if candidate_direction[0] != 0 and n.value == '|':
                continue
            if candidate_direction[1] != 0 and n.value == '-':
                continue
            valid_n.append(n)
        if len(valid_n) > 1:
            raise ValueError("Fork in path")
        if len(valid_n) == 0:
            raise ValueError("Fake turn")
        return valid_n[0], (valid_n[0].pos_x - current_node.pos_x, valid_n[0].pos_y - current_node.pos_y)
    if len(f_n) == 0:
        raise ValueError("Fake turn")
    return f_n[0], (f_n[0].pos_x - current_node.pos_x, f_n[0].pos_y - current_node.pos_y)


def traverse(start_node: Node, nodes: Dict[Tuple[int, int], Node]) -> Sequence[Node]:
    """
    Function that iterates through the map by starting from first node, expanding its neighbours and checking if we
    have a valid situation depending on the value of that node - if that's not satisfied than an error is thrown.

    :param start_node: Starting node on the map - inferred from `load_nodes` map
    :param nodes: Nodes that represent the map
    :return: Final full path of the nodes
    """
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
            current_node, direction = uppercase_handler(
                current_node=current_node,
                nodes=nodes,
                neighbours=neighbours,
                direction=direction
            )
        elif current_node.value == _CORNER:
            current_node, direction = corner_handler(
                current_node=current_node,
                neighbours=neighbours,
                direction=direction
            )
        elif current_node.value in [_VERTICAL_DIRECTION, _HORIZONTAL_DIRECTION]:
            current_node = dash_handler(current_node=current_node, direction=direction, nodes=nodes)
            if current_node is None:
                raise ValueError("Invalid corner")
        else:
            raise ValueError("Invalid char")


def main(file_path: str) -> Tuple[str, str]:
    """
    Main "wrapper" function

    :param file_path: Path to the file
    :return: List of visited letters and list of full path chars
    """
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
