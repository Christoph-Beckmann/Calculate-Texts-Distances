import re
import pandas as pd
from time import time
from rapidfuzz import fuzz
from pathlib import Path

# Global Variables 
resfolder = Path("./res/")
text1file = "text1.txt"
lvsth_distance_text1 = 19
text2file = "text2.txt"
lvsth_distance_text2 = 28

# Edit:
datafile = "data_2.xlsx"
texts_swapped = True

def load_texts(file: Path) -> str:
    """
    Load the text from a file.
    
    :param file: Path object representing the file to load the text from.
    :return: The content of the file as a string.
    """
    with file.open("r") as f:
        return f.read()

def load_data(file: Path) -> pd.DataFrame:
    """
    Load participant data into a DataFrame.
    
    :param file: Path object representing the data file.
    :return: A DataFrame containing participant data.
    """
    return pd.read_excel(
        file,
        dtype = {"VP": int, "text1": str, "text2": str}
    ).reset_index(drop=True)

def words(text: str) -> list:
    """
    Extract words and punctuation from a text.
    
    :param text: The text to extract words and punctuation from.
    :return: A list of words and punctuation marks found in the text.
    """
    pattern = r"[\w']+|[.,!?;]"
    return re.findall(pattern, text)

def compare_texts(text1: str, text2: str, data: pd.DataFrame, swapped: bool) -> pd.DataFrame:
    """
    Compare each text from the participant data with the provided texts and calculate the token-based similarity metrics.

    :param text1: The first text for comparison.
    :param text2: The second text for comparison.
    :param data: A DataFrame containing participant data.
    :param swapped: A boolean flag indicating if the texts were swapped during the study.

    :return: A DataFrame containing the updated participant data with the calculated similarity metrics.
    """
    for index, row in data.iterrows():
        participant = row['lfdnr']
        digital_bool = row['digital_bool']
        pp_text1 = " ".join(row['text1'].split())
        pp_text2 = " ".join(row['text2'].split())

        data.loc[index, 'vp'] = int(str(digital_bool)+str(participant))
        data.loc[index, 'text1'] = pp_text1
        data.loc[index, 'text2'] = pp_text2

        if not swapped:
            lvsth_distance_1 = fuzz.token_set_ratio(words(pp_text1), words(text1))
            lvsth_distance_2 = fuzz.token_set_ratio(words(pp_text2), words(text2))
            prefix = ""
        else:
            lvsth_distance_1 = fuzz.token_set_ratio(words(pp_text2), words(text1))
            lvsth_distance_2 = fuzz.token_set_ratio(words(pp_text1), words(text2))
            prefix = "_rev"

        data.loc[index, f'lvsth_distance_T1{prefix}'] = lvsth_distance_1
        data.loc[index, f'percent_change_T1{prefix}'] = ((lvsth_distance_1-lvsth_distance_text1)/lvsth_distance_text1)*100
        data.loc[index, f'lvsth_distance_T2{prefix}'] = lvsth_distance_2
        data.loc[index, f'percent_change_T2{prefix}'] = ((lvsth_distance_2-lvsth_distance_text2)/lvsth_distance_text2)*100

    return data

def save_data(new_data: pd.DataFrame, folder: Path):
    """
    Save the updated DataFrame to an Excel file.
    
    :param new_data: The updated DataFrame containing participant data and calculated similarity metrics.
    :param folder: The folder in which to save the Excel file.
    """
    new_data.to_excel(folder / f'Calc_error_counts_{int(time())}.xlsx', index=False)

def main(): 
    """
    Main function that loads the texts and participant data, compares the texts, calculates similarity metrics,
    and saves the updated participant data to an Excel file.
    """
    text1 = load_texts(resfolder / text1file)
    text2 = load_texts(resfolder / text2file)
    data = load_data(resfolder / datafile)
    new_data = compare_texts(text1, text2, data, texts_swapped) 
    save_data(new_data, resfolder)


if __name__ == "__main__":
    main()