from __future__ import annotations

from items import *
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, List, Dict, Callable
from collections.abc import Iterable, Iterator

# add print responsibility decorator pattern

from items import *


class ReceiptIterator(Iterator):
    def __init__(self, receipt: Receipt) -> None:
        self._collection = receipt.get_receipt()
        self._position = 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += 1
        except IndexError:
            raise StopIteration()
        return value


class Receipt(Iterable):
    items: List

    def __iter__(self) -> ReceiptIterator:
        return ReceiptIterator(self)

    def __init__(self, items: List = None) -> None:
        self.items = [] if items is None else items

    def __getitem__(self, index: int) -> Item:
        return self.items[index]

    def __str__(self) -> str:
        return "Receipt:\n" \
               + "\n".join(["Name: " + i.name + " Units: " + str(i.unit)
                            + " Price" + str(i.per_price) + " Total: " + str(i.total)
                            for i in self.items]) + "\n" \
               + "Sum: " + str(sum([i.total for i in self.items]))

    def get_receipt(self):
        return self.items

    def add_item(self, item: List[Item]):
        self.items.extend(item)

    def get_items_count(self) -> Dict[Item: int]:
        counter = {}
        for i in self.items:
            counter[i] = 1 if i not in counter else counter[i] + 1
        return counter

    def get_items(self) -> List[Item]:
        return self.items


def calculate_receipt_total(receipt: Receipt) -> int:
    return sum([i.total for i in receipt])


def calculate_receipt_discounts(receipt: Receipt) -> int:
    for disc in ALL_DISCOUNTS:
        disc(receipt.get_items())
    pass


@dataclass
class Report:
    cash_register: CashRegister

    @abstractmethod
    def report(self) -> str:
        pass


@dataclass
class XReport(Report):

    def report(self) -> str:
        revenue = sum(self.cash_register.amounts)
        count_items = self.cash_register.items_sold_num
        return "X Report: \n" + \
               "Total Revenue: " + str(revenue) + "\n" \
               + "\n".join([str(item) + " | " + str(sold) for item, sold in count_items.items()])


@dataclass
class ZReport(Report):

    def report(self) -> str:
        self.cash_register.clear()
        return "Z report: \n"


class CashRegister:
    amounts: List[int]
    items_sold_num: Dict[Item: int]

    def __init__(self, amounts: List[int] = None, items_sold_num: Dict[Item: int] = None):
        self.amounts = [] if amounts is None else amounts
        self.items_sold_num = {} if items_sold_num is None else items_sold_num

    def clear(self):
        self.amounts = []
        self.items_sold_num = {}

    def sold_items(self, receipt: Receipt, amount: int):
        for item, count in receipt.get_items_count().items():
            self.items_sold_num[item] = count if item not in self.items_sold_num \
                else self.items_sold_num[item] + count
        self.amounts.append(amount)


@dataclass
class Cashier:

    @staticmethod
    def generate_report(cash_register: CashRegister) -> None:
        print(ZReport(cash_register).report())

    @staticmethod
    def open_receipt() -> Receipt:
        return Receipt()

    @staticmethod
    def add_item_to_open_receipt(item: List[Item], receipt: Receipt) -> None:
        receipt.add_item(item)

    @staticmethod
    def print_receipt(receipt: Receipt) -> None:
        print(receipt)

    @staticmethod
    def close_receipt(receipt: Receipt, total_amount: int, cash_register: CashRegister) -> Receipt:
        cash_register.sold_items(receipt, total_amount)
        return receipt

    @staticmethod
    def calculate_receipt(receipt: Receipt, calculation_method: Callable = calculate_receipt_total):
        return calculation_method(receipt)


@dataclass
class Store:
    ITEMS = [
        Item(MILK, per_price=5),
        Item(MILK, per_price=5, unit=3),
        Item(BEER, per_price=8),
        Item(BEER, per_price=8, unit=6),
        Item(BEER, per_price=8, unit=8),
        Item(MINERAL_WATER, per_price=0.5),
        Item(MINERAL_WATER, per_price=0.5, unit=6),
        Item(MINERAL_WATER, per_price=0.5, unit=12),
        Item(BREAD, per_price=1),
        Item(BREAD, per_price=1, unit=3),
        Item(DIAPERS, per_price=7),
        Item(DIAPERS, per_price=7, unit=2),
    ]
