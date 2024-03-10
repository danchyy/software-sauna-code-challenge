# Solution Overview

## Code Walkthrough

The main function is called `traverse` and that's where iteration through the map happens.

I also have an additional dataclass to store the data about the chars on map:

```
@dataclass
class Node:
    value: str
    pos_x: int
    pos_y: int
```

The algorithm is as follows:

```
startNode, nodes := loadNodes(loadMap('name_of_file.txt'))
while True:
    currentNode := startNode
    neighbours := expand(startNode)
    for
```

### LOADER METHODS

I have defined two loader methods, `load_map_from_file` reads the file and content from it to a list of strings. That string data is then passed to `load_nodes` function that parses string data into a dictionary that maps position of letters to a `Node` instance. 


### NODE EXPANDERS

Function that collects neighboring nodes.

### NODE HANDLERS

These functions are used to correctly perform a functionality that is tied to each different type of characters/tokens found along the map. We have `uppercase_handler`, `corner_handler` and `dash_handler`. 

`uppercase_handler` determines whether the path needs to continue straight through or turn, the `corner_handler` function checks if we have a proper setup for turning 90 deegrees, if not it throws an error, and `dash_handler` is in charge of checking `-` and `|` chars and its appropriate errors.



## Installation/Setup

To setup use Python's venv, but you can go without it as the only real requirement is `pytest`.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
```

## Run Tests

`pytest tests`

This runs tests for all of the example maps that are given in the instruction text for the task.

