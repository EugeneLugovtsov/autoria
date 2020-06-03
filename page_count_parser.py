# -*- coding: utf-8 -*-
#
#  Project autoria
#  time: 07.05.2020
#
#  Powered by Eugene Lugovtsov
#  e-mail: lug.zhenia@gmail.com


# Parser for determining the number of pages
class PageCountParser:

    @staticmethod
    def parse(page):
        # First you need to find all the items labeled "mhide".
        # And the value we need will be in the last element
        page_count = page.find_all("span", class_="mhide")[-1].get_text()
        # If such elements are not found, then we send that we have only one page
        return int(page_count) if page_count.isnumeric() else 1
