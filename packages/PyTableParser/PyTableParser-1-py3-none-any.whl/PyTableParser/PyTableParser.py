"""
This file contains code for the programming library "PyTableParser".
Author: GlobalCreativeApkDev
"""

# Importing necessary libraries.
import copy
import os
import sys
import mpmath
from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True


# Creating necessary functions.


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


def get_index_of_elem(a_list: list, elem: object) -> int:
    for i in range(len(a_list)):
        if a_list[i] == elem:
            return i
    return -1


def is_number(obj: object) -> bool:
    try:
        mpf(str(obj))
        return True
    except ValueError:
        return False


def select_query_to_condition(table_attributes, select_query):
    # type: (list, str) -> (list, Condition or None)
    """
    Example 1: select * from Character where max_hp > 125
    Example 2: select name from Character where max_hp > 125
    Example 3: select id,name from Character where max_hp > 125
    """

    query_words: list = select_query.split(" ")
    if query_words[0] != "select":
        raise Exception("Invalid select query! First word must be 'select'!")

    attributes: list = []  # initial value:
    if query_words[1] == "*":
        attributes = table_attributes
    else:
        attribute_words: list = query_words[1].split(",")
        for a in attribute_words:
            attributes.append(a)

    if query_words[2] != "from":
        raise Exception("Invalid select query! Third word must be 'from'!")

    if len(query_words) > 4:
        if query_words[4] != "where":
            raise Exception("Invalid select query! Third word must be 'where'!")

        if len(query_words) != 8:
            raise Exception("Cannot get select query condition! Length of the query must be 8 words!")
        return attributes, Condition(query_words[5], query_words[6], query_words[7])
    else:
        return attributes, None


def parse_pytable_file(pytable_file):
    # type: (str) -> PyTable
    if pytable_file[len(pytable_file) - 8:] != ".pytable":
        raise Exception("Invalid file extension '" + str(pytable_file.split(" ")[1]) + "'! Must be '.pytable' file!")
    f = open(pytable_file, 'r')
    lines: list = f.readlines()
    table_name: str = pytable_file.split(".")[0]
    attributes: list = []  # initial value
    data: list = []  # initial value
    for i in range(len(lines)):
        curr_line: str = lines[i]
        if i == 0:
            # Get the attributes
            line_words: list = curr_line.split("|")[1:-1]
            for i in range(len(line_words)):
                line_words[i] = line_words[i].strip()

            attributes = line_words
        else:
            # Get the data
            curr_data: list = curr_line.split("|")[1:-1]
            for k in range(len(curr_data)):
                curr_data[k] = curr_data[k].strip()

            data.append(curr_data)

    return PyTable(table_name, attributes, data)


# Creating necessary classes.


class PyTable:
    """
    This class contains attributes of a PyTable class object.
    """

    def __init__(self, name, attributes, data=None):
        # type: (str, list, list) -> None
        if data is None:
            data = []
        self.name: str = name
        self.__attributes: list = attributes
        if len(data) > 0:
            if not isinstance(data[0], list) or len(data[0]) != len(attributes):
                raise Exception("PyTable initialisation error! Length of attributes and data row mismatch!")

        self.__data: list = data

    def __str__(self):
        # type: () -> str
        return str(self.name).upper() + "\n" + \
               str(tabulate([self.__attributes] + self.__data, headers='firstrow', tablefmt='fancy_grid'))

    def get_nth_row(self, n):
        # type: (int) -> str
        return str(self.name).upper() + "\n" + \
               str(tabulate([self.__attributes] + self.__data[n - 1], headers='firstrow', tablefmt='fancy_grid'))

    def insert_values(self, values):
        # type: (list) -> None
        for i in range(len(self.__attributes) - len(values)):
            values.append(None)

        self.__data.append(values)

    def select_attributes_where(self, attribute_list, conditions=None):
        # type: (list, list) -> str
        if conditions is None:
            conditions = []
        selected_attributes: list = attribute_list
        selected_data: list = []  # initial value
        if len(conditions) == 0:
            for row in self.__data:
                curr_add: list = []  # initial value
                for k in row:
                    for s in selected_attributes:
                        if get_index_of_elem(self.__attributes, s) == get_index_of_elem(row, k):
                            curr_add.append(k)
                            break

                selected_data.append(curr_add)
        else:
            for row in self.__data:
                all_conditions_met: bool = True  # initial value
                for condition in conditions:
                    first_value: object = row[get_index_of_elem(self.__attributes, condition.attribute_name)]
                    if not condition.evaluate(first_value):
                        all_conditions_met = False
                        break
                if all_conditions_met:
                    curr_add: list = []  # initial value
                    for k in row:
                        for s in selected_attributes:
                            if get_index_of_elem(self.__attributes, s) == get_index_of_elem(row, k):
                                curr_add.append(k)
                                break

                    selected_data.append(curr_add)

        return str(self.name).upper() + "\n" + \
               str(tabulate([selected_attributes] + selected_data, headers='firstrow', tablefmt='fancy_grid'))

    def get_attributes(self):
        # type: () -> list
        return self.__attributes

    def get_data(self):
        # type: () -> list
        return self.__data

    def clone(self):
        # type: () -> PyTable
        return copy.deepcopy(self)


class Condition:
    """
    This class contains attributes of a selection condition.
    """

    ALLOWED_OPERATORS: list = [">", "<", "==", "!=", ">=", "<=", "in", "contains", "starts with", "ends with"]

    def __init__(self, attribute_name, operator, other_value):
        # type: (str, str, str or int or float or mpf) -> None
        self.attribute_name: str = attribute_name
        self.operator: str = operator
        self.other_value: str or int or float or mpf = other_value

    def evaluate(self, first_value):
        # type: (object) -> bool
        if self.operator == ">":
            if is_number(first_value) and is_number(self.other_value):
                return mpf(first_value) > mpf(self.other_value)
            return False
        elif self.operator == "<":
            if is_number(first_value) and is_number(self.other_value):
                return mpf(first_value) < mpf(self.other_value)
            return False
        elif self.operator == "==":
            if is_number(first_value) and is_number(self.other_value):
                return mpf(first_value) == mpf(self.other_value)
            return False
        elif self.operator == "!=":
            if is_number(first_value) and is_number(self.other_value):
                return mpf(first_value) != mpf(self.other_value)
            return False
        elif self.operator == ">=":
            if is_number(first_value) and is_number(self.other_value):
                return mpf(first_value) >= mpf(self.other_value)
            return False
        elif self.operator == "<=":
            if is_number(first_value) and is_number(self.other_value):
                return mpf(first_value) <= mpf(self.other_value)
            return False
        elif self.operator == "in":
            return str(first_value) in str(self.other_value)
        elif self.operator == "contains":
            return str(self.other_value) in str(first_value)
        elif self.operator == "starts with":
            return str(first_value)[0:len(str(self.other_value))] == str(self.other_value)
        elif self.operator == "ends with":
            return str(first_value)[len(str(first_value)) -
                                                            len(str(self.other_value)):] == str(self.other_value)
        else:
            return False

    def __str__(self):
        # type: () -> str
        return str(self.attribute_name) + " " + str(self.operator) + " " + str(self.other_value)

    def clone(self):
        # type: () -> Condition
        return copy.deepcopy(self)


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    print("Welcome to 'PyTableParser' by 'GlobalCreativeApkDev'.")
    print("This library is used to parse '.pytable' files.")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_using: str = input("Do you want to continue using 'PyTableParser'? ")
    while continue_using == "Y":
        clear()
        pytable_file: str = input("Please enter the name of the '.pytable' file you want to parse: ")
        print(parse_pytable_file(pytable_file))
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_using = input("Do you want to continue using 'PyTableParser'? ")

    return 0


if __name__ == '__main__':
    main()
