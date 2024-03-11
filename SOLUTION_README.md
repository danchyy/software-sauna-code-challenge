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

#### Corner Handler

Function checks if we have a proper setup for turning 90 deegrees, if not it throws an exception for either:

* Fork 
* Fake Turn

It also handles a complex situation which I thought it should be correct but wasn't mentioned in examples:

```
 -   @
 +---D
 |
 x
```

When the path reaches `+` this shouldn't cause an error or exception since the right side
(or up) of the corner contains an invalid sign. I'm not sure if that should be considered as an exception because
it's an invalid map or if it should be okay because it doesn't obstruct the remainder of the path.

So the solution for this situation would be: `@D---+|x`. I have more similar examples in my test maps:

* dummy.txt
* reverse.txt
* tough_corner.txt
* ultra_compact.txt

#### Uppercase Handler 

Determines whether the path needs to continue straight through or turn. The Uppercase chars
should be handled either as `+` or `|`/`-`. I didn't add the same "complex corner" handling in situations
such as: 

```
 +----+  @ 
 P--+ +-M+ 
    A------+
        x  |
        |  |
        +--+
          
```

Because in situation when we reach letter `M` we would have to look deep into the node-map
to determine if the `-` below the `M` is just part of an intersection and thus a valid option/route (as in this situation)
or if it's an invalid continutation, and we should keep the direction.

It actually isn't that complicated to check that but we would simply need to recurse multiple times
in order to check if that node is valid.


#### Dash Handler

In charge of checking `-` and `|` chars and its appropriate errors. Main exception check
is to check that orientation of dashes is correct based on the direction of the path and surrounding nodes.


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

## Run single map

From the root folder simply call:

`python .\src\main.py --path=.\maps\tough.txt`