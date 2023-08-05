"""
This file contains code for the application "PyAutoCoder".
Author: GlobalCreativeApkDev
"""


# Application version: 0.0.1


# Importing necessary libraries.


import os
import sys
import re
import mpmath
from mpmath import mp, mpf

mp.pretty = True


# Creating necessary functions.


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


def write_a_program_that_prints_the_sum_of_the_first_n_numbers(n: int) -> str:
    response: str = ""  # initial value
    response += """
sum: int = 0  # initial value
for i in range(1, """ + str(int(n) + 1) + """):
    sum += n
    
print(sum)
"""
    return response


def write_a_function_that_prints_the_sum_of_the_elements_in_a_list() -> str:
    return """
def sum_of_list_elements(a_list: list) -> mpf:
    sum: mpf = mpf("0")
    for elem in a_list:
        sum += mpf(elem)
        
    return sum    
"""


def write_a_program_that_prints_the_product_of_the_first_n_numbers(n: int) -> str:
    response: str = ""  # initial value
    response += """
sum: int = 1  # initial value
for i in range(1, """ + str(int(n) + 1) + """):
    sum *= n

print(sum)
"""
    return response


def write_a_function_that_prints_the_product_of_the_elements_in_a_list() -> str:
    return """
def product_of_list_elements(a_list: list) -> mpf:
    product: mpf = mpf("1")
    for elem in a_list:
        product *= mpf(elem)

    return product    
"""


def write_a_function_that_checks_whether_a_string_is_a_palindrome_or_not() -> str:
    return """
def is_palindrome(s: str) -> bool:
    return s == s[::-1]
"""


def write_a_function_that_gets_the_number_of_substring_occurrences_in_a_string() -> str:
    return """
def num_occurrences(string: str, substring: str) -> int:
    return len(string.split(substring)) - 1    
"""


def write_a_program_that_prints_a_random_integer_between_a_and_b_inclusive(a: int, b: int) -> str:
    response: str = ""  # initial value
    response += """
import random
print(random.randint(""" + str(a) + """, """ + str(b) + """)
"""
    return response


def write_a_program_that_prints_a_random_number_between_a_and_b(a: mpf, b: mpf) -> str:
    response: str = ""  # initial value
    response += """
    import random
    print(mpf(""" + str(a) + """) + random.random() * mpf(""" + str(b - a) + """))
    """
    return response


def parse(request: str) -> str:
    if re.search("Write a program that prints the sum of the first .* numbers!", request):
        try:
            return write_a_program_that_prints_the_sum_of_the_first_n_numbers(int(request.split(" ")[10]))
        except ValueError:
            return "Sorry! We cannot respond to your request!"
    elif re.search("Write a function that prints the sum of the elements in a list!", request):
        return write_a_function_that_prints_the_sum_of_the_elements_in_a_list()
    elif re.search("Write a program that prints the product of the first .* numbers!", request):
        try:
            return write_a_program_that_prints_the_product_of_the_first_n_numbers(int(request.split(" ")[10]))
        except ValueError:
            return "Sorry! We cannot respond to your request!"
    elif re.search("Write a function that prints the product of the elements in a list!", request):
        return write_a_function_that_prints_the_product_of_the_elements_in_a_list()
    elif re.search("Write a function that checks whether a string is a palindrome or not!", request):
        return write_a_function_that_checks_whether_a_string_is_a_palindrome_or_not()
    elif re.search("Write a function that gets the number of substring occurrences in a string!", request):
        return write_a_function_that_gets_the_number_of_substring_occurrences_in_a_string()
    elif re.search("Write a program that prints a random integer between .* and .* inclusive!", request):
        try:
            return write_a_program_that_prints_a_random_integer_between_a_and_b_inclusive(int(request.split(" ")[9]),
                                                                                      int(request.split(" ")[11]))
        except ValueError:
            return "Sorry! We cannot respond to your request!"
    elif re.search("Write a program that prints a random number between .* and .*!", request):
        try:
            return write_a_program_that_prints_a_random_number_between_a_and_b(int(request.split(" ")[9]),
                                                                                      int(request.split(" ")[11][:-1]))
        except ValueError:
            return "Sorry! We cannot respond to your request!"
    else:
        return "Sorry! We cannot respond to your request!"


# Creating main function used to run the application.


def main() -> int:
    """
    The main function used to run the application.
    :return: an integer
    """

    print("Welcome to 'PyAutoCoder v0.0.1' by 'GlobalCreativeApkDev'.")
    print("This application is used to automatically generate Python code based on user's request.")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_using: str = input("Do you want to continue using 'PyAutoCoder v0.0.1'? ")
    while continue_using == "Y":
        clear()
        request: str = input("> ")
        print(parse(request))
        print("\n")
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_using = input("Do you want to continue using 'PyAutoCoder v0.0.1'? ")

    return 0


if __name__ == '__main__':
    main()

