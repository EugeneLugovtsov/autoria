# -*- coding: utf-8 -*-
#
#  Project autoria
#  time: 07.05.2020
#
#  Powered by Eugene Lugovtsov
#  e-mail: lug.zhenia@gmail.com
import csv


# This class implements saving data to csv file.
class CarsSaver:

    @staticmethod
    def save(file_path, data):
        # use the with construct to automate file closure
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            # First you need to write the column names in the file.
            # To do this, we take the keys from the first line in data.
            writer.writerow(list(data[0].keys()))
            for car in data:
                # Go through the data and save the data line by line to a file
                writer.writerow(list(car.values()))
