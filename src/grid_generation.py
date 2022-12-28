""""""

from .grid import Grid, Field
from random import shuffle, choice


def _possible_values(grid: Grid, x: int, y: int):
    possibles = []
    for i in range(1, 10):
        if grid.can_be_at(i, x, y):
            possibles.append(i)
    return tuple(possibles)


def random_grid_generator() -> Grid:
    """"""
    empty_fields = []

    for i in range(9):
        for j in range(9):
            empty_fields.append(Field(i, j, 0))

    generated_grid = None

    try:
        _fill_grid(Grid(empty_fields))
    except _GridGenerated as generated:
        generated_grid = generated.grid

    return generated_grid


def values_emptier(grid: Grid, empties: int) -> Grid:
    """"""
    assert 81 > empties > 0, "Počet prázdných musí být v intervalu [1; 80]"
    for _ in range(empties):
        choice(grid.filled_fields).value = 0
    return grid


def _fill_grid(grid: Grid) -> Grid:
    """"""
    for x in range(9):
        for y in range(9):
            field = grid.field(x, y)
            if field.is_empty:
                possibles = list(_possible_values(grid, field.x, field.y))
                shuffle(possibles)
                for value in possibles:
                    field.value = value
                    _fill_grid(grid)
                    field.value = 0
                return grid

    raise _GridGenerated(grid)


class _GridGenerated(Exception):
    """"""

    def __init__(self, grid: Grid):
        """"""
        self.__grid = grid

    @property
    def grid(self) -> Grid:
        """"""
        return self.__grid
