from pandas import DataFrame
import re

# Use A Dictionary. Create A Default Dictionary. First iterate Through The First Sentence
# In The Text File Which Will Include The Headers. Save The As Keys In The Default Dictionary
# Go To The Next Sentence. The First Word Corresponds To The Column
# If There Is No Value, The Cell Will Take The Average For The Row
# If The Line Contains Too Few, Then We Will Fill In The Last Cell With The Average
# If There Are More Cells Than Headers Then We Are Missing A Header. Create A New Unknown Header

# The Dictionary Value Will Be A List, Which We Will Append New Values Too

# Once The Process Is Complete We Will Use The Dictionary And Convert Into A Pandas
# DataFrame

# We Will Customize CSV's In The Following Ways:
# i)   Account for | (Tabular CSV's)
# ii)  Account For Comma's Within Quotation Marks " Therefore, I am" Could Erronously
#      Be Split. We Will Have a Boolean Definition Which Engages When We Hit A Quotation
#      Thereby Precluding Splitting When the Boolean Is Engaged. After An Unquote When
#      The Bool Is Disengaged, When We Encounter A Comma, We Can Split As Normal

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

def create_data_frame(file_name):
    with open(file_name, "r", encoding='utf-8-sig') as f_handle:
        # Empty Cells Will Need To Have An Average Of All Values: Come Back To This
        average = 0

        # The Data Frame Dictionary Will Be Used To Create A Pandas DataFrame
        data_frame_dictionary = {}
        #data_frame_dictionary.setdefault("Unknown_Label", [])

        # List Of Column Headings Allows Us To Reference The Array As We Store Data Into The Correct Column
        column_headings = []

        # Create The Lines Object (The Entire Data Split Into Sentences)
        sentences = f_handle.readlines()

        # We Need To Keep Track Of Quotation Marks, As Delimiters Symbols Which Are Surrounded By Quotation
        # Marks Must Be Ignored.
        quotation_obj = quotation_search()

        # Counter == 0 Allows Us Check The First Row, Which Is Needed For Headers
        counter = 0
        for line in sentences:
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

                split_columns = split(line.rstrip(), split_location)

                for column in split_columns:
                    column = re.sub(r'^"|"$', '', column)
                    column_headings.append(column)
                    data_frame_dictionary[column] = []
                counter = counter + 1
            # Dealing With The Data (Row 1 +) And Not Headers
            else:
                for char_position, char in enumerate(line):
                    if char == "\"":
                        quotation_obj.quotation_encountered()
                    # A Comma Engaged Unbounded By Quotation Marks Is A Split Point
                    # Record The Location In The Line So We Can Split It
                    if char == delimiter and quotation_obj.is_quotation_engaged() == False:
                        split_location.append(char_position)

                split_data = split(line.rstrip(), split_location)
                for i in range(len(split_data)):
                    if split_data[i] == " ":
                        data_frame_dictionary[column_headings[i]].append(average)
                    else:
                        split_data[i] = re.sub(r'^"|"$', '', split_data[i])
                        data_frame_dictionary[column_headings[i]].append(split_data[i])

    return data_frame_dictionary

file_name = ["barometer-1617.csv", "indoor-temperature-1617.csv", "outside-temperature-1617.csv","rainfall-1617.csv"]

i = 0
data_frame = None
for file in file_name:
    data_frame_dictionary = create_data_frame(file)
    print(data_frame_dictionary)
    frame = DataFrame(data_frame_dictionary)
    if i == 0:
        data_frame = frame
        i = i + 1
    else:
        # Not All Of The Data Frames Have The Same Number Of Rows. The Default Position
        # For Merge Is To Delete Rows Which Are Uncommon To The Data Frames Being Merged
        data_frame = DataFrame.merge(frame, data_frame, on="DateTime", how='right').fillna(0)

print(data_frame)




# Make Sure All of The Rows Are Unique

