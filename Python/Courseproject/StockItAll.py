#!/usr/bin/env python3

"""
This module contains classes and methods used to maintain and manipulate StockItems

Author: 4gnusd3i
License: MIT
"""


class StockItem:
    """
    The StockItem class contains the recipe for creating items and concatenating object attributes into one formatted
    string, for improved readability.

    Attributes:
        code: An integer representing the item's code
        description: A string describing the item
        amount: An integer representing the amount of the item
    """

    def __init__(self, code=None, description=None, amount=None):
        self.code = code
        self.description = description
        self.amount = amount

    # Method for concatenating all values in a StockItem object
    def item_info(self):
        """This method returns a formatted string that consists of all the values for one StockItem object."""
        return "{:<6}{:^64}{:>6}".format(self.code, self.description, self.amount)

    # Represents the usage of the StockItem constructor
    def __repr__(self):
        return "StockItem({}, {}, {})".format(self.code, self.description, self.amount)


class StockTracker:
    """
    The StockTracker class is responsible for storing all the StockItem objects
    and providing methods for manipulating them.

    Attributes:
        item_list: An empty list used to store StockItems
    """

    def __init__(self):
        self.item_list = list()

    # Method for adding StockItem objects from CLI
    def add_item_cli(self):
        """
        This method uses 'Code, Description and Amount' separated by ',' from user input provided
        through the CLI in main.py.
        On correct input it will create a StockItem object and append it to the item_list.
        On incorrect input it will raise a ValueError and inform the user to try again.
        """
        item = input("\nUse the following syntax: Code, Description, Amount\n")
        try:
            StockItem.code, StockItem.description, StockItem.amount = item.split(",")
            self.item_list.append(StockItem(StockItem.code, StockItem.description, StockItem.amount))
            print("\nItem successfully added")
        except ValueError:
            print("\nCould not add item, try again with the correct syntax!")

    # Method for adding StockItem objects from Server-client
    def add_item_server(self, data):
        """
        This method takes 'Code, Description and Amount' separated by ',' from user input provided
        from client.py, that's received by the server running in main.py.
        The received data will be used to create a StockItem object, which will then be appended to the item_list.

        Args:
            data: The input string

        Returns:
            None
        """
        StockItem.code, StockItem.description, StockItem.amount = data.split(",")
        self.item_list.append(StockItem(StockItem.code, StockItem.description, StockItem.amount))

    # Method for showing all objects in item_list
    def show_all_items(self):
        """
        This method prints a formatted header string and a divider, before iterating through the item_list
        to display all stored StockItem objects using the item_info format.
        """
        print("\n{:<6}{:^64}{:>6}".format("Code", "Description", "Amount"))
        print("----------------------------------------------------------------------------")
        for item in self.item_list:
            print("{}".format(item.item_info()))

    # Method for retrieving the index of an object in item_list
    def get_index(self, code):
        """
        This method takes 'Code' passed from either show_item() or update_item_amount(). It then enumerates
        the StockItem objects in item_list to find the index position matching the object that contains
        the correct item.code.

        Args:
            code: The item.code

        Returns:
            i: The index
        """
        for i, item in enumerate(self.item_list):
            if item.code == code:
                return i

    # Method for updating an object item.amount
    def update_item_amount(self):
        """
        This method uses 'Code' from user input provided through the CLI in main.py. It then passes this as an argument
        to get_index() and uses the return value as the local index variable. By the use of another user input, the
        input received is used to update the objects item.amount at the corresponding index. If the 'Code' entered
        by the user does not match an item.code contained by an object, a ValueError will be raised and the user
        will be informed.

        Returns:
            None
        """
        code = input("\nEnter the item-code: ")
        index = StockTracker.get_index(self, code)
        change_to = input("Enter the new item-amount: ")
        try:
            self.item_list[index].amount = change_to
            print("\nItem-amount successfully changed")
        except TypeError:
            print("\nERROR: THERE IS NO ITEM WITH THAT ITEM-CODE!")

    # Method for showing an object based on its index
    def show_item(self):
        """
        This method uses 'Code' from user input provided through the CLI in main.py. It then passes this as an argument
        to get_index() and uses the return value as the local index variable. The object that contains the inputted
        item.code will the be displayed. If the 'Code' entered by the user does not match an item.code contained by an
        object, a ValueError will be raised and the user will be informed.

        Returns:
            None
        """
        code = input("\nEnter the items code: ")
        index = StockTracker.get_index(self, code)
        try:
            print("\n{:<6}{:^64}{:>6}".format("Code", "Description", "Amount"))
            print("----------------------------------------------------------------------------")
            print(self.item_list[index].item_info())
        except TypeError:
            print("\nERROR: THERE IS NO ITEM WITH THAT ITEM-CODE!")
