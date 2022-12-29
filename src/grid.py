"""Tento modul obsahuje samotnou definici pravidel hry sudoku.

Obsahuje definice dvou entit - políčka (třídy `Field`) a hrací plochy (třídy
`Grid`). Nad rámec definice těchto struktur jsou instance těchto tříd vybaveny
jednoduchými nástroji pro snazší manipulaci s těmito objekty.
"""

from typing import Iterable


class Field:
    """Instance této třídy reprezentují každé jednotlivé políčko hrací plochy.
    Každé políčko je někde na hrací ploše umístěno (má souřadnice v osách `x`
    a `y`) a má nějakou hodnotu.

    Tato hodnota může nabývat libovolného celého čísla v rozmezí intervalu
    `[1, 9]`, přičemž také může jít o prázdné políčko, které se značí hodnotou
    `0`, která je jinak neplatná.
    """

    # Povolené hodnoty, kterých může políčko nabývat; interval [1, 9]
    __AVAILABLE_VALUES = [i for i in range(10)]

    def __init__(self, x: int, y: int, value: int):
        """Initor políčka, který přijímá souřadnice os `x` a `y` (počítáno od
        `0`) a hodnoty políčka, která smí nabývat pouze hodnot v intervalu
        `[0, 9]`, přičemž hodnota `0` odpovídá prázdnému políčku.
        """
        self.__x = x
        self.__y = y
        self.__value = value

    @property
    def x(self) -> int:
        """Souřadnice osy `x` tohoto políčka"""
        return self.__x

    @property
    def y(self) -> int:
        """Souřadnice osy `y` tohoto políčka"""
        return self.__y

    @property
    def value(self) -> int:
        """Hodnota tohoto políčka"""
        return self.__value

    @value.setter
    def value(self, new_value: int):
        """Setter pro nastavení hodnoty políčka. Pokud není tato hodnota
        platnou (tedy v intervalu [0, 9], kde 0 odpovídá prázdnému políčku),
        pak je vyhozena výjimka.
        """
        if new_value not in self.__AVAILABLE_VALUES:
            raise ValueError(f"Hodnota '{new_value}' není povolena!")
        self.__value = new_value

    @property
    def is_empty(self) -> bool:
        """Vrací, zda-li je políčko prázdné či nikoliv"""
        return self.value == 0

    def __repr__(self) -> str:
        """Vrací textovou reprezentaci políčka. Používá k tomu znaku podtržítka
        pro prázdné políčko, jinak vrací hodnotu políčka.
        """
        return "_" if self.is_empty else str(self.__value)


class Grid:
    """"""

    def __init__(self, fields: Iterable[Field]):
        """"""
        self.__fields = tuple(fields)
        assert len(self.fields) == 81, "Hrací plocha musí mít 81 políček!"

    @property
    def fields(self) -> tuple[Field]:
        """"""
        return self.__fields

    @property
    def empty_fields(self) -> tuple[Field]:
        """"""
        return tuple([f for f in self.fields if f.is_empty])

    @property
    def filled_fields(self) -> tuple[Field]:
        """"""
        return tuple([f for f in self.fields if not f.is_empty])

    @property
    def num_of_empty_fields(self) -> int:
        """"""
        return len(self.empty_fields)

    @property
    def rows(self) -> tuple[tuple[Field]]:
        """"""
        rows = []
        for y in range(9):
            rows.append(self.row(y))
        return tuple(rows)

    @property
    def columns(self) -> tuple[tuple[Field]]:
        """"""
        cols = []
        for x in range(9):
            cols.append(self.column(x))
        return tuple(cols)

    def field(self, x: int, y: int) -> Field:
        """"""
        for field in self.fields:
            if field.x == x and field.y == y:
                return field
        raise ValueError(f"Políčko se souřadnicemi [{x}, {y}] neexistuje!")

    def column(self, x: int) -> tuple[Field]:
        """"""
        fields_in_column = []
        for field in self.fields:
            if field.x == x:
                fields_in_column.append(field)
        return tuple(fields_in_column)

    def row(self, y: int) -> tuple[Field]:
        """"""
        fields_in_row = []
        for field in self.fields:
            if field.y == y:
                fields_in_row.append(field)
        return tuple(fields_in_row)

    def small_square(self, x: int, y: int) -> tuple[Field]:
        """"""
        # Zjištění levého horního políčka v malém čtverci
        base_x = (x // 3) * 3
        base_y = (y // 3) * 3

        fields_in_square = []

        for i in range(3):
            for j in range(3):
                fields_in_square.append(self.field(base_x + i, base_y + j))

        return tuple(fields_in_square)

    def can_be_at(self, value: int, x: int, y: int) -> bool:
        """"""
        # Test unikátnosti hodnoty v řádku
        if value in [f.value for f in self.row(y)]:
            return False

        # Test unikátnosti hodnoty ve sloupci
        elif value in [f.value for f in self.column(x)]:
            return False

        # Test unikátnosti hodnoty v malém čtverci
        elif value in [f.value for f in self.small_square(x, y)]:
            return False

        # Pokud hodnota prošla všemi třemi testy
        return True

    def __repr__(self):
        """"""
        rows = []
        for i in range(9):
            rows.append(" ".join([str(f) for f in self.row(i)]))
        return "\n".join(rows)
