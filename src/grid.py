""""""

from typing import Iterable


class Field:
    """"""

    __AVAILABLE_VALUES = [i for i in range(10)]

    def __init__(self, x: int, y: int, value: int):
        """"""
        self.__x = x
        self.__y = y
        self.__value = value

    @property
    def x(self) -> int:
        """"""
        return self.__x

    @property
    def y(self) -> int:
        """"""
        return self.__y

    @property
    def value(self) -> int:
        """"""
        return self.__value

    @value.setter
    def value(self, new_value: int):
        """"""
        if new_value not in self.__AVAILABLE_VALUES:
            raise ValueError(f"Hodnota '{new_value}' není povolena!")
        self.__value = new_value

    @property
    def is_empty(self) -> bool:
        """"""
        return self.value == 0

    def __repr__(self) -> str:
        """"""
        return str(self.__value)


class Grid:
    """"""

    def __init__(self, fields: Iterable[Field]):
        """"""
        self.__fields = tuple(fields)

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

    def field(self, x: int, y: int) -> Field:
        """"""
        for field in self.fields:
            if field.x == x and field.y == y:
                return field



