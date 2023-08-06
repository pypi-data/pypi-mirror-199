from abc import ABCMeta, abstractmethod

from fastapi_listing.typing import TableModelTyp


class DaoAbstract(metaclass=ABCMeta):

    @abstractmethod
    def create(self, values: dict[str, str | int]) -> TableModelTyp:
        pass

    @abstractmethod
    def update(self, identifier: dict[str, str | int | list], values: dict) -> bool:
        pass

    @abstractmethod
    def read(self, identifier: dict[str, str | int | list], fields: list | str = "__all__") -> TableModelTyp:
        pass

    @abstractmethod
    def delete(self, ids: list[int]) -> bool:
        pass
