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

        # Vytvoření hluboké kopie dodané hrací plochy
        grid = grid.copy

        # Opakuj tolikrát, kolik má být vyprázdněno políček
        for _ in range(self.num_of_empty_values):

            # Náhodně vyber již vyplněné políčko a nastav mu hodnotu na 0
            choice(grid.filled_fields).value = 0

        # Vrať výsledek
        return grid

    @abstractmethod
    def generate(self) -> Grid:
        """Abstraktní metoda odpovědná za stanovení závazné signatury, která
        má být potomky této třídy implementována.

        Implementace potomků této třídy jsou odpovědné za vybudování úplné a
        konzistentní konfigurace hrací plochy."""

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


class BacktrackingGenerator(GridGenerator):
    """Jednoduchý náhdoný generátor rozložení hry sudoku, který je postaven
    na elementárním algoritmu, tzv. 'backtracking'. Ten je rekurzivní analogií
    na prohledávání do hloubky (Depth-First Search, DFS).
    """

    def generate(self) -> Grid:
        """Metoda implementující abstraktní metodu předka. Je odpovědná za
        vybudování náhodné kombinace hodnot hry sudoku.

        Samotná implementace pro zpřehlednění syntaxe využívá prostředků
        výjimky typu `_GridGenerated`, pomocí které dokáže vrátit první
        nalezenou konzistentní kombinaci - 'vyřešenou' hru.

        Celkové těžiště výpočtu této metody je však delegováno do metody
        `__fill_grid(Grid) -> Grid`.
        """
        generated_grid = None

        try:
            self.__fill_grid(self.empty_grid)
        except _GridGenerated as generated:
            generated_grid = generated.grid

        return generated_grid

    def __fill_grid(self, grid: Grid) -> Grid:
        """Samotný výpočet náhodné, úplné a konzistentní hrací plochy pro
        sudoku. Pomocná delegace výpočetních prostředků.
        """

        # Pro všechny kombinace souřadnic `x` a `y`
        for x in range(9):
            for y in range(9):
                field = grid.field(x, y)

                # Pokud je políčko prádzné
                if field.is_empty:

                    # Zjisti hodnoty, kterými dané políčko může být vyplněno
                    # a zamíchej je (prvek náhody)
                    possibles = self.possible_values(grid, field.x, field.y)
                    shuffle(possibles)

                    # Pro každou takovou hodnotu ji vyzkoušej a rekurzivně
                    # se zavolej (další iterace)
                    for value in possibles:
                        field.value = value
                        self.__fill_grid(grid)

                        # Pokud řešení nebylo nalezeno, nastav tuto hodnotu
                        # zpět na 0, tedy na nevyplněné políčko
                        field.value = 0
                    return grid

        # Bylo nalezeno řešení. Pro předejití "nekonečného" běhu vyhoď výjimku
        raise _GridGenerated(grid)


class _GridGenerated(Exception):
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
