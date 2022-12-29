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

    # Povolené hodnoty, kterých může políčko nabývat; interval [0, 9]
    __AVAILABLE_VALUES = [i for i in range(10)]

    def __init__(self, x: int, y: int, value: int):
        """Initor políčka, který přijímá souřadnice os `x` a `y` (počítáno od
        `0`) a hodnoty políčka, která smí nabývat pouze hodnot v intervalu
        `[0, 9]`, přičemž hodnota `0` odpovídá prázdnému políčku.
        """
        # Test, že jsou souřadnice korektní, v rozmezí intervalu [0, 8]
        assert x in range(9)
        assert y in range(9)

        # Test, že hodnota políčka je v rozmezí itervalu [0, 9] (0 pro prázdné)
        assert value in self.__AVAILABLE_VALUES

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
        # Test, že dodaná nová hodnota je v povoleném intervalu ([0, 9])
        assert new_value in self.__AVAILABLE_VALUES

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
    """Instance této třídy reprezentují hrací plochu hry sudoku.
    Hrací plocha se sestává ze sady políček, která jsou opatřena kromě hodnoty
    i vlastními souřadnicemi v osách `x` a `y`. Díky tomu lze mezi nimi
    vyhledávat, filtrovat a libovolně tyto sdružovat.
    """

    def __init__(self, fields: Iterable[Field]):
        """Initor, který přijímá sadu políček, ze kterých je hrací plocha
        sestavena. Pokud políček není validní počet (tedy 81) je vyhozena
        výjimka.
        """
        self.__fields = tuple(fields)

        # Test, že počet dodaných políček odpovídá 81
        assert len(self.fields) == 81

    @property
    def fields(self) -> tuple[Field]:
        """N-tice políček, ze kterých se hrací plocha sestává."""
        return self.__fields

    @property
    def empty_fields(self) -> tuple[Field]:
        """N-tice prázdných políček, ze kterých se hrací plocha sestává."""
        return tuple([f for f in self.fields if f.is_empty])

    @property
    def filled_fields(self) -> tuple[Field]:
        """N-tice vyplněných políček, ze kterých se hrací plocha sestává."""
        return tuple([f for f in self.fields if not f.is_empty])

    @property
    def num_of_empty_fields(self) -> int:
        """Počet prázdných políček."""
        return len(self.empty_fields)

    @property
    def rows(self) -> tuple[tuple[Field]]:
        """Dvourozměrná n-tice, která sdružuje políčka uspořádaná dle řádků.
        """
        rows = []
        for y in range(9):
            rows.append(self.row(y))
        return tuple(rows)

    @property
    def columns(self) -> tuple[tuple[Field]]:
        """Dvourozměrná n-tice která sdružuje políčka uspořádaná dle sloupců.
        """
        cols = []
        for x in range(9):
            cols.append(self.column(x))
        return tuple(cols)

    def field(self, x: int, y: int) -> Field:
        """Metoda odpovědná za vyhledání konkrétního políčka dle souřadnic
        `x` a `y`. Pokud takové políčko není nalezeno, je vyhozena výjimka.
        """
        for field in self.fields:
            if field.x == x and field.y == y:
                return field
        raise ValueError(f"Políčko se souřadnicemi [{x}, {y}] neexistuje!")

    def column(self, x: int) -> tuple[Field]:
        """Metoda, která se pokusí vyhledat konkrétní sloupeček z dodané
        souřadnice na ose `x`. Výstupem je tedy vyfiltrovaná n-tice políček,
        kde tato souřadnice odpovídá hodnotě dodaného parametru.
        """
        fields_in_column = []
        for field in self.fields:
            if field.x == x:
                fields_in_column.append(field)
        return tuple(fields_in_column)

    def row(self, y: int) -> tuple[Field]:
        """Metoda, která se pokusí vyhledat konkrétní řádek z dodané
        souřadnice na ose `y`. Výstupem je tedy vyfiltrovaná n-tice políček,
        kde tato souřadnice odpovídá hodnotě dodaného parametru.
        """
        fields_in_row = []
        for field in self.fields:
            if field.y == y:
                fields_in_row.append(field)
        return tuple(fields_in_row)

    def small_square(self, x: int, y: int) -> tuple[Field]:
        """Metoda, která se pokusí vyhledat všechna políčka malého čtverce
        hrací plochy, jehož políčko o dodaných souřadnicích je součástí.

        Princip funkce je takový, že se vyhledá z dodaných souřadnic levý
        horní roh příslušného malého čtverce a následně se pouze transpozičně
        dohledají políčka v tomto čtverci.

        Výstupem je n-tice těchto políček.
        """
        # Zjištění levého horního políčka v malém čtverci
        base_x = (x // 3) * 3
        base_y = (y // 3) * 3

        fields_in_square = []

        for i in range(3):
            for j in range(3):
                fields_in_square.append(self.field(base_x + i, base_y + j))

        return tuple(fields_in_square)

    def can_be_at(self, value: int, x: int, y: int) -> bool:
        """Metoda odpovědná za ověření, zda-li by dodaná hodnota na dodaných
        souřadnicích pro tuto hrací plochu nenarušila konzistenci hry.

        Tato konzistence odpovídá třem jednoduchým obecným pravidlům, tedy:

        - unikátnost hodnoty v řádku
        - unikátnost hodnoty ve sloupečku
        - unikátnost hodnoty v malém čtverci

        Pokud je kterékoliv z těchto pravidel porušeno, je vrácena hodnota
        `False`, jinak `True`.
        """
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

    def __repr__(self) -> str:
        """Metoda odpovědná za reprezentaci hrací plochy coby textového
        řetězce. Celkovým výstupem této metody je transformace hrací plochy
        na jednotlivé hodnoty políček uspořádané po řádcích, přičemž jsou
        hodnoty v řádku odděleny mezerami.
        """
        rows = []
        for i in range(9):
            rows.append(" ".join([str(f) for f in self.row(i)]))
        return "\n".join(rows)
