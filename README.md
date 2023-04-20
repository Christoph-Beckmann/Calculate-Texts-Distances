# Text Comparison Tool for Master Thesis

This text comparison tool is designed to assist in the evaluation of texts within the context of a master's thesis. It uses token-based similarity metrics to compare and analyze texts, making it easier to identify differences and similarities between them.

## Table of Contents

1. [Description](#description)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

## Description

The main goal of this text comparison tool is to facilitate the analysis of textual data within the context of a master's thesis. It is particularly useful for researchers working with large text datasets, as it provides a streamlined and efficient method for comparing and contrasting textual data.

The tool is implemented in Python and utilizes the `rapidfuzz` library for token-based similarity metrics, allowing for a more accurate comparison of texts. Additionally, it leverages the `pandas` library for efficient data manipulation and the `pathlib` library for easy file management.

## Requirements

- Python 3.6 or higher
- rapidfuzz
- pandas
- pathlib

## Installation

1. Clone this repository or download it as a ZIP file.
2. Make sure you have Python 3.6 or higher installed on your system.
3. Install the required libraries by running the following command in your terminal:

```shell
pip install rapidfuzz pandas
```

## Usage

1. Place your text files and participant data file (in Excel format) in the res/ folder.
2. Update the global variables in the script to match your file names and any other settings you'd like to change.
3. Run the script using the following command in your terminal: `python3 main.py`
4. The script will generate a new Excel file with the comparison results in the res/ folder.