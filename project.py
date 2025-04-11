import csv
import os
import sys

from tabulate import tabulate
from datetime import date
import random


class CSVManager:
    """
    Manages CSV file operation
    """
    def __init__(self, file, fieldnames):
        """
        Initializes CSV file and creates a new one if it does not exist
        :param file: CSV file path
        :param fieldnames: (list) Column headers
        """
        self.file = file
        self.fieldnames = fieldnames
        self.data = []

        if not os.path.exists(self.file):
            with open(self.file, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
                writer.writeheader()

        self.read()

    def read(self):
        """
        Read data from CSV file into memory
        """
        with open(self.file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            self.data = [row for row in reader]

        return self.data

    def append(self, row):
        """
        Appends a new row into the CSV file
        :param row: (dict) Data to be added into the csv file(must match the fieldnames)
        """
        with open(self.file, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writerow(row)
        self.data.append(row)

    def overwrite(self, new_data):
        """
        Replace all the data in the CSV file
        :param new_data: (list) list of dictionaries to be recorded
        """
        with open(self.file, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(new_data)
        self.data = new_data

    def __str__(self):
        """
        :return: formatted table of data
        """
        return tabulate(self.data, headers="keys", tablefmt="pretty")


def main():
    """
    Main program entry point
    """
    inventory_manager = CSVManager("inventory.csv", ["Item", "Quantity", "Price"])
    sales_manager = CSVManager(
        "sales.csv", ["Date", "Transaction ID", "Items", "Total"]
    )

    while True:
        main_menu = [
            {"Menu": "Manage Warehouse", "Shortcut": "W"},
            {"Menu": "Store Mode", "Shortcut": "S"},
            {"Menu": "Transaction Database", "Shortcut": "T"},
            {"Menu": "Exit Program", "Shortcut": "E"},
        ]

        print(tabulate(main_menu, headers="keys", tablefmt="pretty"))
        try:
            user_choice = input("Action: ").lower()

            if user_choice == "w":
                warehouse_mode(inventory_manager)
            elif user_choice == "s":
                store_mode(inventory_manager, sales_manager)
            elif user_choice == "t":
                report(sales_manager)
            elif user_choice == "e":
                sys.exit("Thank you for using the program.")
            else:
                raise ValueError

        except ValueError:
            pass

# Warehouse mode functions
def warehouse_mode(shop):
    """
    Menu for inventory management
    :param shop: (CSVManager) Instance that handles the inventory
    """
    warehouse_menu = [
        {"Menu": "Add an Item", "Shortcut": "A"},
        {"Menu": "Remove an Item", "Shortcut": "R"},
        {"Menu": "View Inventory", "Shortcut": "V"},
        {"Menu": "Go back to Main Menu", "Shortcut": "B"},
    ]

    print(tabulate(warehouse_menu, headers="keys", tablefmt="pretty"))
    try:
        user_choice = input("Action: ").lower()

        if user_choice == "a":
            add_item(shop)
        elif user_choice == "r":
            deduct_item(shop)
        elif user_choice == "v":
            report(shop)
        elif user_choice == "b":
            main()
        else:
            raise ValueError

    except ValueError:
        pass


def add_item(shop):
    """
    Adds a new item into the inventory
    Automatically updates the CSV file
    :param shop: (CSVManager) Instance that handles the inventory
    """
    while True:
        item = input("What item will you add? ").title()
        quantity = input("How many will you have in stock? ")
        price = float(input("How much will it cost? "))

        new_item = {"Item": item, "Quantity": quantity, "Price": f"{price:.2f}"}

        shop.append(new_item)

        while True:
            try:
                back = input("Do you want to add another item? (y/n): ")
                if back == "n":
                    warehouse_mode(shop)
                if back == "y":
                    break
                else:
                    raise ValueError
            except ValueError:
                pass


def deduct_item(shop):
    """
    Removes an item into the inventory
    Automatically updates the CSV file
    :param shop: (CSVManager) Instance that handles the inventory
    """
    while True:
        item_sub = input("What will be remove from the inventory? ").title()
        new_data = [row for row in shop.data if row["Item"] != item_sub]
        shop.overwrite(new_data)

        while True:
            try:
                back = input("Do you want to remove another item? (y/n): ")
                if back == "n":
                    warehouse_mode(shop)
                if back == "y":
                    break
                else:
                    raise ValueError
            except ValueError:
                pass


def report(file):
    """
    Displays the data in table form
    :param file: (CSVManager) Instance that handles the inventory or sales report
    """
    while True:
        print(file)

        while True:
            try:
                back = input("Do you want to back to Main Menu? (y/n): ")
                if back == "y":
                    main()
                else:
                    raise ValueError
            except ValueError:
                pass

# Store mode functions
def store_mode(shop, sales):
    """
    Processes all the transactions
    Updates the inventory in real time
    :param shop: (CSVManager) Instance that handles the inventory
    :param sales: (CSVManager) Instance that handles the sales report

    """
    while True:
        total = float()
        cart = []
        transaction_id = (str(date.today())).replace("-", "") + str(
            random.randint(100000, 9999999)
        )
        print('Enter "Done" to print the receipt.')

        while True:
            purchase = input("Item: ").title()

            if purchase == "Done":
                break
            for item in shop.data:
                item["Quantity"] = int(item["Quantity"])
                item["Price"] = round(float(item["Price"]), 2)

            found = False # Switch to find if input is in the inventory

            for item in shop.data:
                if purchase == item["Item"]:
                    found = True
                    if item["Quantity"] == 0:
                        print(f"{purchase} is out-of-stock.")
                    else:
                        item["Quantity"] -= 1
                        total += item["Price"]
                        cart.append({"Item": item["Item"], "Price": item["Price"]})
                        save_data = [
                            {
                                "Item": item["Item"],
                                "Quantity": str(item["Quantity"]),
                                "Price": f"{item['Price']:.2f}",
                            }
                            for item in shop.data
                        ]
                        shop.overwrite(save_data) # Updates the csv file for inventory

            if not found:
                print(f"{purchase} is not available in this store.")

        # Updates the csv file for transaction records
        items = ", ".join([item["Item"] for item in cart])
        row = {
            "Date": date.today(),
            "Transaction ID": transaction_id,
            "Items": items,
            "Total": f"{total:.2f}",
        }
        sales.append(row)

        #Process the receipt
        rows = [[item["Item"], f"{item['Price']:.2f}"] for item in cart]
        rows.append(["TOTAL", f"{total:.2f}"])
        rows.insert(-1, ["-" * 10, "-" * 6])
        rows.append(["Trans. ID", transaction_id])
        print(
            tabulate(
                rows, headers=["Items", "Price"], tablefmt="outline", numalign="right"
            )
        )
        print("Thank you!\n")

        while True:
            try:
                back = input("Process another? (y/n) : ")
                if back == "n":
                    main()
                if back == "y":
                    break
                else:
                    raise ValueError
            except ValueError:
                pass


if __name__ == "__main__":
    main()
