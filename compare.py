from time import time
from rapidfuzz.distance import Levenshtein
import re
import pandas as pd
import time

# Global Variables 
resfolder = "./res/"
text1file = "text1.txt"
lvsth_distance_text1 = 19
text2file = "text2.txt"
lvsth_distance_text2 = 28

# Edit:
datafile = "data_2.xlsx"
texts_swapped = True


def loadtexts():
    """
    Load texts from files.

    :return text1: loaded text 1
    :return text2: loaded text 2 
    """

    try:
        with open(resfolder + text1file,"r") as f:
            text1 = f.read()
    except Exception as error:
        print("Error in loading text 1: " + str(error))

    try:
        with open(resfolder + text2file, "r") as f:
            text2 = f.read()
    except Exception as error:
        print("Error in loading text 2: " + str(error))

    return text1, text2 

def loaddata():
    """
    Load Participant data into dataframe with pandas. 

    :return data: dataframe of participant data
    """

    try:
        data = {}
        data = pd.read_excel(
            resfolder + datafile,
            dtype = {"VP": int, "text1": str, "text2": str}
            )
    
        data.reset_index()

    except Exception as error:
        print("Error in loading dataset: " + str(error))

    return data

def words(text: str):
    pattern = r"[\w']+|[.,!?;]"
    return re.findall(pattern,text)

def compare_texts(text1: str, text2: str, data: pd.DataFrame, swapped: bool ):
    """
    Compare each text from data with text1 and text2. Return founded errors. 

    :param text1: Correct Text 1 
    :param text2: Correct Text 2
    :param data: dataframe of participant data

    :return data: new dataframe
    """

    for index, row in data.iterrows():
        # get participant data into variables to pass as parameter in levenshtein function.
        # split each words, and replace empty spaces.
        participant = row['lfdnr']
        digital_bool = row['digital_bool']
        pp_text1 = " ".join(row['text1'].split())
        pp_text2 = " ".join(row['text2'].split())

        # create unique VP-Code with lfdnr and digital_bool-value
        data.loc[index, 'vp'] = int(str(digital_bool)+str(participant))

        # Replace participant text with participant text without spaces.
        data.loc[index,'text1'] = pp_text1
        data.loc[index,'text2'] = pp_text2

        if swapped == False:
            lvsth_distance_1 = Levenshtein.distance(words(pp_text1), words(text1))
            lvsth_distance_2 = Levenshtein.distance(words(pp_text2), words(text2))

            data.loc[index,'lvsth_distance_T1'] = lvsth_distance_1
            data.loc[index, 'percent_change_T1'] = ((lvsth_distance_1-lvsth_distance_text1)/lvsth_distance_1)*100
            data.loc[index,'lvsth_distance_T2'] = lvsth_distance_2
            data.loc[index, 'percent_change_T2'] = ((lvsth_distance_2-lvsth_distance_text2)/lvsth_distance_2)*100
        else:    # Switch compared text, because we changed texts in week 3. 
            lvsth_distance_1 = Levenshtein.distance(words(pp_text2), words(text1))
            lvsth_distance_2 = Levenshtein.distance(words(pp_text1), words(text2))

            data.loc[index,'lvsth_distance_T1_rev'] = lvsth_distance_1
            data.loc[index, 'percent_change_T1_rev'] = ((lvsth_distance_1-lvsth_distance_text2)/lvsth_distance_1)*100
            data.loc[index,'lvsth_distance_T2_rev'] = lvsth_distance_2
            data.loc[index, 'percent_change_T2_rev'] = ((lvsth_distance_2-lvsth_distance_text1)/lvsth_distance_2)*100 

    return data

def save_data(new_data: pd.DataFrame):
    """
    Saving new dataframe into excel file.

    :param new_data: New dataframe
    """

    try:
        new_data.to_excel(resfolder + 'Calc_error_counts_{}.xlsx'.format(int(time.time())))
    except Exception as error:
        print( "Error in saving new dataset: " + str(error) )

### Main

if __name__ == "__main__":
    text1, text2 = loadtexts()
    data = loaddata()
    new_data = compare_texts(text1, text2, data, texts_swapped) 
    save_data(new_data)
