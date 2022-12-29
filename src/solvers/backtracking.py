""""""

from src import SolverAlgorithm, Grid
from src.solver import SolutionFound


class BacktrackingSolver(SolverAlgorithm):
    """Instance této třídy slouží pro řešení hry sudoku metodou prostého
    backtrackingu.
    """

    def solve(self, grid: Grid) -> Grid:
        """Metoda řídící hledání řešení. V rámci rekurzivního (backtracking)
        prohledávání je odpovědná za odchycení výjimky, která slouží jako
        nejsnazší způsob probublání řešení až do volající instance.
        """
        # Vytvoření kopie hrací plochy
        grid = grid.copy

        try:
            # Začni rekurzivně prohledávat - to vyústí ve výjimku
            self.__backtrack(grid)
        except SolutionFound as solution_exception:
            # Vrať nalezené řešení
            return solution_exception.grid
        else:
            # Pokud výjimka o nalezeném řešení nebyla vyhozena
            raise Exception("Řešení neexistuje!")

    def __backtrack(self, grid: Grid):
        """Rekurzivní hledání jednoho řešení hrací plochy, tedy takové
        konfigurace, která bude úplná a konzistentní.
        """
        # Pro všechny kombinace souřadnic `x` a `y`
        for x in range(9):
            for y in range(9):
                current_field = grid.field(x, y)

                # Pokud je políčko prádzné
                if current_field.is_empty:

                    # Vyzkoušej každou hodnotu, zda-li ji lze použít. Pokud
                    # ano, nastav ji pro toto políčko a rekurzivně pokračuj,
                    for value in range(1, 10):
                        if grid.can_be_at(value, x, y):
                            current_field.value = value
                            self.__backtrack(grid)

                            # Pokud tudy cesta nevede, nastav zpět na 0
                            current_field.value = 0

                    # Pro toto políčko byly vyzkoušeny všechny hodnoty,
                    # zkus se tedy vrátit
                    return grid

        # Bylo nalezeno řešení. Pro předejití "nekonečného" běhu vyhoď výjimku
        raise SolutionFound(grid)


