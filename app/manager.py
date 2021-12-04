from cashier import *

YES = "y"
NO = "n"


class Manager:
    @staticmethod
    def ask_manager_for_x_report() -> bool:
        return input("Generate X report? (y/n)") == YES

    @staticmethod
    def ask_manager_for_z_report() -> bool:
        return input("Generate Z report? (y/n)") == YES

    @staticmethod
    def generate_report(cash_register: CashRegister) -> None:
        print(XReport(cash_register).report())
