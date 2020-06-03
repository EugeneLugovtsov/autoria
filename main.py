# -*- coding: utf-8 -*-
#
#  Project autoria
#  time: 07.05.2020
#
#  Powered by Eugene Lugovtsov
#  e-mail: lug.zhenia@gmail.com

import requests
import multiprocessing
from bs4 import BeautifulSoup

from cars_per_page_parser import CarsPerPageParser
from page_count_parser import PageCountParser
from new_car_parser import NewCarParser
from cars_saver import CarsSaver


def get_html(url, params=None):
    # Getting the html of the necessary page
    return requests.get(url, params=params).text


# Function responsible for parsing all pages
def parse(data):
    # Get the BeautifulSoup object for later use
    soup = BeautifulSoup(get_html(data[0], {"page": data[1]}), "html.parser")
    # We create object of a NewCarParser which parse information about new car
    new_car_parser = NewCarParser()

    cars = []
    # We go through each machine on the page and parse its data
    for car_card in CarsPerPageParser.parse(soup):
        # Add data about each car to the general list
        cars.append(new_car_parser.parse(car_card))

    print(f"Successfully parsing page number {data[1]}.")
    return cars


# Entry point into the program, it is responsible for the business logic of the parser
if __name__ == '__main__':
    url = input("URL: ").strip()
    file_path = input("File Path: ").strip()

    # Create a soup object and look for the number of pages of this car brand
    soup = BeautifulSoup(get_html(url), "html.parser")
    page_count = PageCountParser.parse(soup)

    print(f"Number of pages = {page_count}.")

    data = []

    # Create a pool of threads for parallel processing of all pages.
    # We use the with construction to automatically close the pool
    with multiprocessing.Pool(processes=3) as pool:
        for cars in pool.imap(parse, zip([url for i in range(page_count)], range(1, page_count + 1))):
            # Add data about the machine to the global list
            data.extend(cars)

    # Save information about all cars of a given brand
    CarsSaver.save(file_path, data)
    print(f"Successfully saving the results.")
