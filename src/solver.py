"""Tento modul obsahuje definici řešitelů hry sudoku.

Především pak definuje obecný abstraktní protokol pro všechny řešitele
abstraktní třídou `SolverAlgorithm`.
"""

from abc import ABC, abstractmethod
from src import Grid


class SolverAlgorithm(ABC):
    """Abstraktní třída, jejíž instance představují objekty schopné poskytovat
    službu řešení hry sudoku. Slouží jako obecná deklarace signatury metody
    `solve(Grid) -> Grid`, která převádí neúplné rozložení na úplné; při
    zachování konzistence."""

    @abstractmethod
    def solve(self, grid: Grid) -> Grid:
        """Abstraktní metoda, která stanovuje signaturu metody, která má být
        potomky této třídy implementována. Jejím cílem je poskytovat funkci
        převodu neúplné, leč konzistentní konfigurace hrací plochy na úplnou.
        """


class SolutionFound(Exception):
    """Pomocná výjimka pro usnadnění přístupu v rámci rekurzivního výpočtu.
    Jejím hlavním smyslem je získat možnost postoupit vybudovanou hrací plochu
    i napříč backtracking-based výpočtem pro zpřehlednění kódu.
    """

    def __init__(self, grid: Grid):
        """Initor, který přijímá vybudovanou úplnou a konzistentní konfiguraci
        hry."""
        self.__grid = grid

    @property
    def grid(self) -> Grid:
        """Vlastnost vracející přijatou úplnou a konzistentní nově
        vygenerovanou konfiguraci."""
        return self.__grid


