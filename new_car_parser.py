# -*- coding: utf-8 -*-
#
#  Project autoria
#  time: 07.05.2020
#
#  Powered by Eugene Lugovtsov
#  e-mail: lug.zhenia@gmail.com


# The parser finds all the necessary information about the car
class NewCarParser:

    @staticmethod
    def _parse_photo(car_card):
        # Link to the photo of the car marked with "proposition_photo"
        return {
            "photo": car_card.find("div", class_='proposition_photo').find("source").get("srcset")
        }

    @staticmethod
    def _parse_car_title(car_card):
        # Title of the car is split by title and equip
        # and marked with "proposition_name" and "proposition_equip" respectively
        return {
            "title": car_card.find("h3", class_="proposition_name").get_text().strip(),
            "equip": car_card.find("div", class_="proposition_equip").get_text().strip()
        }

    @staticmethod
    def _parse_car_information(car_card):
        # Information regarding the type of fuel,
        # gearbox and drive is provided in the proposition_information section.
        # It is worth noting that they are not always present,
        # in such cases all passes will be replaced by a symbol -
        information = car_card.find("div", class_="proposition_information").get_text().split("•")
        # Get information length
        information_len = len(information)

        return {
            "fuel": information[0].strip() if information_len >= 1 else "-",
            "transmission": information[1].strip() if information_len >= 2 else "-",
            "drive": information[2].strip() if information_len >= 3 else "-"
        }

    @staticmethod
    def _parse_car_badges(car_card):
        # budgets show whether a car is available or not, and whether credit is also possible.
        # However, information may not be available.
        badges = car_card.find("div", class_="proposition_badges").find_all("span")
        # Get badges length. It is necessary to understand what data are missing
        badges_len = len(badges)

        return {
            "in_stock": badges[0].get_text().strip().replace(" • ", "") if badges_len >= 1 else "-",
            "credit": badges[1].get_text().strip() if badges_len >= 2 else "-"
        }

    @staticmethod
    def _parse_car_price(car_card):
        # This function parses the price box.
        # The price is presented in USD and in UAH.
        # However, sometimes the price may not be available and instead it will be written "Price the price"
        price = car_card.find("div", class_="proposition_price").find_all("span")

        # Determine whether the price is present or not
        if len(price) != 1:
            # Also avoid parsing discounts
            index = 1 if len(price) > 3 else 0
            price_in_usd = price[index].get_text().strip()
            price_in_uah = price[index + 2].get_text().strip()
        else:
            # If there is no price
            price_in_usd = price[0].get_text().strip()
            price_in_uah = price[0].get_text().strip()
        return {
            "price_in_usd": price_in_usd,
            "price_in_uah": price_in_uah
        }

    @staticmethod
    def _parse_car_location(car_card):
        # Parsing the seller’s location and his name.
        # This information is marked as proposition_region
        location = car_card.find("div", class_="proposition_region").get_text().split("•")
        return {
            "location": location[0].strip(),
            "dealer": location[1].strip()
        }

    def parse(self, page):
        # This is function that combines information taken from all parsers
        data = {}
        data.update(self._parse_photo(page))
        data.update(self._parse_car_title(page))
        data.update(self._parse_car_information(page))
        data.update(self._parse_car_badges(page))
        data.update(self._parse_car_price(page))
        data.update(self._parse_car_location(page))

        return data
