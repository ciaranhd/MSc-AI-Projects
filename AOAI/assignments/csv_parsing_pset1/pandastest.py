import pandas as pd
import re
import numpy as np
import sys
import matplotlib.pyplot as plt
import seaborn as sns

class quotation_search:
    def __init__(self):
        self.state = False
    def quotation_encountered(self):
        if self.state == False:
            self.state = True
        else:
            self.state = False
    def is_quotation_engaged(self):
        return self.state
def split(line, split_location):
    split_list = []
    starting_index = 0
    line.rstrip()
    for location in split_location:
        split_data = line[starting_index: location]
        split_list.append(split_data)
        starting_index = location + 1
    split_data = line[starting_index:]
    split_list.append(split_data)
    return split_list
def delimiter_check(first_sentence):
    if "|" in first_sentence:
        return "|"
    else:
        return ","
def stray_end_comma_adjustment(final_char_position, split_location_array, number_of_columns):
    """ A Line Which Contains A Trailing Comma ("DateTime,"mm",)
        Will Over State The Number of Columns.
        Action: Reduce The Column Count By One"""
    if (final_char_position - 1) == split_location_array[-1]:
         number_of_columns -= 1
    return number_of_columns
def cleanse_split_heading_data(split_columns):
    column_headings = []
    data_frame_dictionary = {}
    for column in split_columns:
        column = re.sub(r'^"|"$', '', column)
        column_headings.append(column)
        data_frame_dictionary[column] = []
    if column_headings[-1] == "":
        column_headings = column_headings[:-1]
    return column_headings, data_frame_dictionary
# encoding='utf-8-sig'
def create_data_frame(file_name):
    with open(file_name, "r", encoding='utf-8-sig') as f_handle:
        # Empty Cells Will Need To Have An Average Of All Values: Come Back To This

        # The Data Frame Dictionary Will Be Used To Create A Pandas DataFrame
        data_frame_dictionary = {}

        # List Of Column Headings Allows Us To Reference The Array As We Store Data Into The Correct Column
        column_headings = []

        # Create The Lines Object (The Entire Data Split Into Sentences)
        sentences = f_handle.readlines()

        # We Need To Keep Track Of Quotation Marks, As Delimiters Symbols Which Are Surrounded By Quotation
        # Marks Must Be Ignored.
        quotation_obj = quotation_search()

        # Counter == 0 Allows Us Check The First Row, Which Is Needed For Headers
        counter = 0
        number_of_columns = 1
        for line in sentences:
            # Ignore Blank Lines
            if line == "\n":
                continue
            delimiter_count = 0
            # The First Row Is The Headers
            split_location = []
            if counter == 0:
                # Establish What The Delimiter Is
                delimiter = delimiter_check(line)
                for char_position, char in enumerate(line):
                    if char == "\"":
                        quotation_obj.quotation_encountered()
                    if char == delimiter and quotation_obj.is_quotation_engaged() == False:
                        split_location.append(char_position)
                        number_of_columns += 1
                # Stray End Comma Adjustment
                number_of_columns = stray_end_comma_adjustment(char_position,split_location,number_of_columns)
                split_columns = split(line.rstrip(), split_location)

                # Cleanse The Split Headers Data
                column_headings, data_frame_dictionary = cleanse_split_heading_data(split_columns)
                counter = counter + 1
            # Dealing With The Data (Row 1 +) And Not Headers
            else:
                for char_position, char in enumerate(line):
                    if char == "\"":
                        quotation_obj.quotation_encountered()
                    # A Comma Engaged Unbounded By Quotation Marks Is A Split Point
                    # Record The Location In The Line So We Can Split It
                    if char == delimiter and quotation_obj.is_quotation_engaged() == False:
                        delimiter_count = delimiter_count + 1
                        # Ignore Columns With No Header
                        if delimiter_count == number_of_columns:
                            break
                        else:
                            split_location.append(char_position)
                split_data = split(line[:char_position].rstrip(), split_location)
                for i in range(len(split_data)):
                    if split_data[i] == "":
                        data_frame_dictionary[column_headings[i]].append(np.nan)
                    else:
                        # Cleanse Data
                        split_data[i] = re.sub(r'^"|"$', '', split_data[i])
                        data_frame_dictionary[column_headings[i]].append(split_data[i])
                row_number_of_columns = len(split_data)
                if row_number_of_columns < number_of_columns:
                    for i in range(row_number_of_columns,number_of_columns):
                        data_frame_dictionary[column_headings[i]].append(np.nan)
    return data_frame_dictionary

file_name = ["barometer-1617.csv", "indoor-temperature-1617.csv", "outside-temperature-1617.csv","rainfall-1617.csv"]
i = 0
data_frame = None
previous_file = None
for file_csv in file_name:
    data_frame_dictionary = create_data_frame(file_csv)
    data_frame_dictionary = pd.DataFrame.from_dict(data_frame_dictionary, orient='index').transpose()
    frame = pd.DataFrame(data_frame_dictionary)
    split_file_name = re.findall(r"[\w']+", file_csv)
    if i == 0:
        data_frame = frame
        i = i + 1
        previous_file = split_file_name[0]
    else:
        # Not All Of The Data Frames Have The Same Number Of Rows. The Default Position
        # For Merge Is To Delete Rows Which Are Uncommon To The Data Frames Being Merged
        data_frame = pd.DataFrame.merge(frame, data_frame, on="DateTime",how='right', suffixes=(f"_{split_file_name[0]}",f"_{previous_file}"))
        previous_file = split_file_name[0]


header = [column for column in data_frame.head(0)]
Averages = [[header, data_frame[header].astype(float).mean(skipna=True),data_frame[header].astype(float).std(skipna=True) ] for header in [column for column in data_frame.head(0)] if header != "DateTime"]
print(Averages)
table = pd.DataFrame(Averages, columns=["DataType", "Averages", "Standard Deviation"])
print(table)

pd.set_option('max_colwidth', 20)

#sns.distplot(data_frame["Temperature_outside"])
#sns.distplot(data_frame["Temperature_range (low)_outside"])
#sns.distplot(data_frame["Temperature_range (high)_outside"])

#sns.distplot(data_frame["Temperature_indoor"])
#sns.distplot(data_frame["Temperature_range (low)_indoor"])
#sns.distplot(data_frame["Temperature_range (high)_indoor"])


