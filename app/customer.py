from __future__ import annotations
from cashier import *
import random
from dataclasses import dataclass

from typing import Any, List

from abc import abstractmethod
from cashier import *

MAX_ITEMS = 10
MIN_ITEMS = 1


class CollectItems:
    @staticmethod
    def collect_items(min_items: int = MIN_ITEMS, max_items: int = MAX_ITEMS) -> List[Item]:
        from numpy.random import choice, randint
        return choice(Store().ITEMS, size=randint(min_items, max_items))


class CollectWalletObjects:
    @staticmethod
    def collect_wallet_objects(cash_min: int = 0,
                               cash_max: int = 200,
                               card_min=0,
                               card_max=300) -> List[WalletObject]:
        from numpy.random import randint
        return [CashWalletObject(randint(cash_min, cash_max)),
                CardWalletObject(randint(card_min, card_max))]


class Payment:
    @staticmethod
    def pay(payment_object: WalletObject, payment_amount: int) -> int:
        payment_object.withdraw(payment_amount)
        print("Customer paid with " + ("cash"
              if payment_object.__class__ == CashWalletObject else "card"))
        return payment_amount


@dataclass
class WalletObject:
    amount: int

    @abstractmethod
    def balance(self) -> int:
        pass

    @abstractmethod
    def withdraw(self, amount: int):
        pass

    @abstractmethod
    def deposit(self, amount: int):
        pass


@dataclass
class CardWalletObject(WalletObject):
    amount: int

    def balance(self) -> int:
        return self.amount

    def withdraw(self, amount: int):
        self.amount -= amount

    def deposit(self, amount: int):
        self.amount += amount


@dataclass
class CashWalletObject(WalletObject):
    amount: int

    def balance(self) -> int:
        return self.amount

    def withdraw(self, amount: int):
        self.amount -= amount

    def deposit(self, amount: int):
        self.amount += amount


@dataclass
class Wallet:
    wallet_objects: List[WalletObject]

    def add_wallet_object(self, wallet_object: WalletObject):
        self.wallet_objects.append(wallet_object)

    def get_wallet_objects(self) -> List[WalletObject]:
        return self.wallet_objects

    def get_wallet_object(self, index) -> WalletObject:
        return self.wallet_objects[index]

    def remove_wallet_object(self, index):
        self.wallet_objects = self.wallet_objects[:index] + self.wallet_objects[index + 1:]


@dataclass
class Customer:
    items: List[Item]
    wallet: Wallet
    receipt: Receipt

    def __init__(self) -> None:
        self.items = CollectItems.collect_items()
        self.wallet = Wallet(CollectWalletObjects.collect_wallet_objects())
        self.receipt = None

    def show_items(self) -> List[Item]:
        return self.items

    def see_receipt(self, receipt: Receipt) -> None:
        self.receipt = receipt

    def pay_by(self) -> WalletObject:
        return self.wallet.get_wallet_object(random.randint(0, len(self.wallet.get_wallet_objects())-1))
