import os, sys
import csv
class CsvHanle():
    def __init__(self):
        return ""

    def read_all_emails_in_csv(self,path,delimiter):
        """
        Read all email of the clients and binding into a list
        :param path: path of csv file
        :return: list of the communication between client and suppporter (conseiller)
        """
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile,delimiter=delimiter)
            discours_id = 1
            row_previous