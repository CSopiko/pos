from dataclasses import dataclass
from typing import List, Dict, Tuple
from abc import abstractmethod

# item names:
MILK: str = "Milk"
MINERAL_WATER: str = "Mineral_Water"
BREAD: str = "Bread"
DIAPERS: str = "Diapers"
BEER: str = "Beer"
ITEM_NAMES_LIST: List = [MILK, MINERAL_WATER, BREAD, DIAPERS, BEER]


@dataclass
class Item:

    def __init__(self, name: str, per_price: float, unit: int = 1, total: int = None):
        self.name = name
        self.per_price = per_price
        self.unit = unit
        self.total = per_price * unit if total is None else total

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.per_price == other.per_price \
               and self.unit == other.unit and self.total == other.total

    def __str__(self) -> str:
        return self.name + "_" + str(self.per_price) + "_" + str(self.unit) + "_" + str(self.total)

    def __hash__(self) -> int:
        return hash(self.name + "_" + str(self.per_price) + "_" + str(self.unit) + "_" + str(self.total))


@dataclass
class Discount:
    percentage: int
    on_items: Dict

    @abstractmethod
    def discount_applies(self, items: List) -> (bool, List[Tuple[Item]], int):
        """
        method checks if discount is available on given items list
        :param items: list of items for discount checking
        :return: whether or not discount is possible,
                discount selected items groups,
                discount percentage
        """
        pass

    def __call__(self, items: List) -> (bool, List[Tuple[Item]], int):
        return self.discount_applies(items)


class BeerDiscount(Discount):
    percentage = 15
    on_items = {Item(BEER, per_price=8, unit=6): 1}

    def discount_applies(self, items: List) -> (bool, List[Tuple[Item]], int):
        possible_discounts = [i for i in items if i in self.on_items]
        if not possible_discounts:
            return False, None, 0
        return True, [tuple(i) for i in possible_discounts], 15


class MilkDiscount(Discount):

    percentage = 20
    on_items = {Item(MILK, per_price=5, unit=3): 1}

    def discount_applies(self, items: List) -> (bool, List[Tuple[Item]], int):
        possible_discounts = [i for i in items if i in self.on_items]
        if not possible_discounts:
            return False, None, 0
        return True, [tuple(i) for i in possible_discounts], 20


class BreadAndWaterDiscount(Discount):
    percentage = 50
    on_items = {Item(MINERAL_WATER, per_price=0.5, unit=6): 2,
                Item(BREAD, per_price=1, unit=3): 1}

    def discount_applies(self, items: List) -> (bool, List[Tuple[Item]], int):
        pass


ALL_DISCOUNTS = [BeerDiscount, MilkDiscount, BreadAndWaterDiscount]
