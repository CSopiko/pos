from manager import *
from customer import *

SHIFTS_NUM = 3
X_REPORT_NUM = 20
Z_REPORT_NUM = 100


def pos_simulation() -> None:
    sim_num = 0
    num_customers = 0
    while sim_num != SHIFTS_NUM:
        shift = True
        store_cashier = Cashier()
        store_manager = Manager()
        store_cash_register = CashRegister()
        while shift:
            store_customer = Customer()
            curr_receipt = store_cashier.open_receipt()
            store_cashier.add_item_to_open_receipt(store_customer.items, curr_receipt)
            store_cashier.print_receipt(curr_receipt)
            payment_amount = store_cashier.calculate_receipt(curr_receipt)
            Payment.pay(store_customer.pay_by(), payment_amount)
            store_cashier.close_receipt(curr_receipt, payment_amount, store_cash_register)
            num_customers += 1
            if num_customers % 20 == 0:
                if store_manager.ask_manager_for_x_report():
                    store_manager.generate_report(store_cash_register)
            if num_customers % 100 == 0:
                if store_manager.ask_manager_for_z_report():
                    store_cashier.generate_report(store_cash_register)
                    shift = False
        sim_num += 1


if __name__ == '__main__':
    pos_simulation()
