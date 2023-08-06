from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Resource(ABC):
    """Abstract Base Class that models a resource-type object"""
    # pylint: disable=redefined-builtin

    def __init__(self, id: int, name: str, type: str):

        self.id = id
        self.name = name
        self._type = type

    def __str__(self):
        return f"Resource of type [{self._type}]. Id: {self.id}. Name: {self.name}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    @abstractmethod
    def info(self) -> dict[str, Any]:
        """Returns information about a Resource

        :rtype: dict
        """

    @abstractmethod
    def key(self) -> str:
        """Abstract method for returning the primary key of a Resource

        :rtype: str
        """

    @abstractmethod
    async def refresh(self) -> None:
        """Refreshes the Resource in case any changes were made independently"""

    @abstractmethod
    async def delete(self) -> None:
        """Deletes the Resource"""
