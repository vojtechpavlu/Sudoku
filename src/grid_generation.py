"""Tento modul obsahuje generátory náhodných rozložení her sudoku. Především
pak obsahuje definici abstraktní třídy `GridGenerator`, která je společným
předkem pro všechny tyto generátory.

Cílem je poskytnout možnost snazšího a dokonalejšího testování strojových
řešitelů hry sudoku.
"""

from .grid import Grid, Field
from random import shuffle, choice
from abc import ABC, abstractmethod


class GridGenerator(ABC):
    """Abstraktní třída `GridGenerator` stanovuje společný protokol pro
    všechny náhodné generátory rozložení her sudoku. Kromě vygenerování
    zcela nového a 'vyřešeného' rozložení také umí připravit hru pro řešení,
    tedy že vyprázdní náhodně některá políčka, která uživatel prostředků
    této třídy může parametricky specifikovat.

    Především pak definuje závaznou signaturu metody `generate() -> Grid`,
    která má za cíl toto rozložení vybudovat.

    Kromě toho také tato definice opatřuje instance metodami pro další
    obsluhu těchto generátorů.
    """

    def __init__(self, num_of_empty_values: int):
        """Initor náhodného generátoru, který v parametru přijímá počet
        políček, která mají být v rámci náhodně vygenerované hry prázdná.

        Tento počet musí být v intervalu 0 (včetně) až 81 (exkluzivně). Lze
        tedy vygenerovat hru, která je zcela vyplněná, vyřešená (pro
        hodnotu 0), stejně jako hru, která má vyplněno pouze jediné políčko.

        Pokud tato podmínka nebude splněna, je vyhozena výjimka `AssertError`.
        """
        # Počet políček k vyprázdnění musí být v intervalu [0, 81)
        assert 0 <= num_of_empty_values < 81
        self.__empty_values = num_of_empty_values

    @property
    def num_of_empty_values(self) -> int:
        """Počet políček, které budou vyprázdněny."""
        return self.__empty_values

    @property
    def empty_grid(self) -> Grid:
        """Vlastnost generující prádzné rozložení, tedy kdy jsou všechna
        políčka hrací plochy prázdná; jejich hodnoty jsou rovny nule.
        """
        # Pomocný kontejner pro prázdná políčka
        empty_fields = []

        # Pro všechny souřadnice os `x` a `y` vygeneruj prázdná políčka, tedy
        # políčka s hodnotou 0
        for x in range(9):
            for y in range(9):
                empty_fields.append(Field(x, y, 0))

        # Vrať grid plný prázdných hodnot
        return Grid(empty_fields)

    def empty_values(self, grid: Grid) -> Grid:
        """Metoda odpovědná za náhodné vyprázdnění některých políček s cílem
        vytvořit z 'vyřešené' hry hádanku.
        """
        # Opakuj tolikrát, kolik má být vyprázdněno políček
        for _ in range(self.num_of_empty_values):

            # Náhodně vyber již vyplněné políčko a nastav mu hodnotu na 0
            choice(grid.filled_fields).value = 0

        # Vrať výsledek
        return grid

    @abstractmethod
    def generate(self) -> Grid:
        """"""

    @staticmethod
    def possible_values(grid: Grid, x: int, y: int) -> list[int]:
        """Statická metoda odpovědná za vrácení seznamu hodnot, kterými lze
        políčko na daných souřadnicích vyplnit.

        K tomu metoda potřebuje sledované rozdělení hry a souřadnice
        sledovaného políčka, tedy souřadnice na osách `x` a `y`.
        """
        possibles = []

        # Pro všechny hodnoty z intervalu [1, 9]
        for potential_value in range(1, 10):

            # Pokud lze tuto hodnotu použít
            if grid.can_be_at(potential_value, x, y):
                possibles.append(potential_value)

        # Vrať seznam hodnot, kterými lze dané políčko vyplnit
        return possibles


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
