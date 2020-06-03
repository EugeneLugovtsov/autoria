# -*- coding: utf-8 -*-
#
#  Project autoria
#  time: 07.05.2020
#
#  Powered by Eugene Lugovtsov
#  e-mail: lug.zhenia@gmail.com


# This parser is looking for all cards with new cars on the page
class CarsPerPageParser:

    @staticmethod
    def parse(page):
        # Cards with information about the car are marked using the "proposition" class
        return page.find_all("div", class_="proposition")
