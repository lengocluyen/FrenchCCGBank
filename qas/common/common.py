# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys
import csv
from qas.text_clustering.contractions import CONTRACTION_MAP_FR
import re

class Utils():
    def expand_contractions(self,text, contraction_mapping):

        contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                          flags=re.IGNORECASE | re.DOTALL)

        def expand_match(contraction):
            match = contraction.group(0)
            first_char = match[0]
            expanded_contraction = contraction_mapping.get(match) \
                if contraction_mapping.get(match) \
                else contraction_mapping.get(match.lower())
            expanded_contraction = first_char + expanded_contraction[1:]
            return expanded_contraction

        expanded_text = contractions_pattern.sub(expand_match, text)
        expanded_text = re.sub("'", "", expanded_text)
        return expanded_text

    def text_clean(self,orginal_text):
        if orginal_text[0] is "'":
            orginal_text = orginal_text[1:]
        if orginal_text[len(orginal_text)-1] is "'":
            orginal_text = orginal_text[:len(orginal_text)-1]
        orginal_text = orginal_text.replace("`","'").replace("''","'").replace("’","'")
        orginal_text = self.expand_contractions(orginal_text,CONTRACTION_MAP_FR)

        return orginal_text

    def read_csv(self, path, output_path, delimiter):
        """

        :param path: path of csv file
        :param delimiter: can be dot virgule
        :param output_path: output of text content
        :return: written content into text file
        :csv: col:0 id discours, col:1 created time, col:2 created by,col:3 subject, col:4 content
        """
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=delimiter)
            all_rows = list(read_csv)
            first_discours_id = int(all_rows[0][0])
            last_discours_id = int(all_rows[len(all_rows)-1][0])
            last_line_in_csv = int(len(all_rows))+1
            current_discours_id = first_discours_id
            line_content=""
            i =1
            previous_row =None
            subject=""
            for row in all_rows:
                i = i + 1
                print ("last_line: %f  %f" %(last_line_in_csv,i))
                if current_discours_id != int(row[0]) and current_discours_id!=last_discours_id:
                    # save into file with name file: discours id,sujet
                    file_name = previous_row[0] + "_" + subject + ".txt"
                    print (file_name)
                    output = os.path.join(output_path, file_name)
                    self.write_txt(output, subject + "\n\n" + line_content)
                    line_content = ""
                elif current_discours_id == last_discours_id and last_line_in_csv==i:
                    # save into file with name file: discours id,sujet
                    line_content += row[2].replace("CLIE", "Client").replace("CONS","Conseiller") + "\n" + self.text_clean(row[4]) + "\n\n"
                    subject = self.text_clean(str(row[3]).replace("re:", "").replace("re :", "").replace("re", "").replace("\t", "").strip())
                    file_name = row[0] + "_" + subject + ".txt"
                    print (file_name)
                    output = os.path.join(output_path, file_name)
                    self.write_txt(output, subject + "\n\n" + line_content)
                    line_content = ""
                line_content += row[2].replace("CLIE", "Client").replace("CONS", "Conseiller") + "\n" + self.text_clean(row[4]) + "\n\n"
                subject = self.text_clean(str(row[3]).replace("re:", "").replace("re :", "").replace("re", "").replace("\t","").strip())

                current_discours_id = int(row[0])
                previous_row = row

    def read_csv_and_output_in_a_list(self, path, delimiter):
        list_discours = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=delimiter)
            discours_id = 1
            row_previous = None
            line_content = ""
            for row in read_csv:
                if discours_id != int(row[0]):
                    # save into file with name file: discours id,sujet
                    subject = str(row_previous[3]).replace("re:", "").strip().replace(" ", "_")

                    list_discours.append(subject + "\n" + line_content)
                    #self.write_txt(output, line_content)
                    line_content = ""
                # line_content: created by - suject \n content
                line_content += row[4] + "\n"
                discours_id = int(row[0])
                row_previous = row
        return list_discours

    def write_txt(self, path, content):
        with open(path, "a") as txt_file:
            txt_file.write(content)


utils = Utils()
utils.read_csv("../data/MAILS_MON_CONSEILLER_CONS.csv", "../data/output/", ";")

