# CSV and TXT Writer Library

This library provides functionality for writing data to CSV and TXT files.

## Functions

### `write_to_csv(data, filename, labels='None')`

This function takes two lists and adds them to a CSV file line by line.

If you choose to add labels, it will add data based on how many label rows there are.

- `data`: Multidimensional list of data for each line.
- `labels`: List of labels for each row (optional).
- `filename`: Name of file.

### `write_to_txt(data, filename, labels='None', char_separator='None')`

This function takes two lists and adds them to a TXT file line by line.

If you choose to add labels, it will add data based on how many label rows there are.

If you choose to add a character separator instead of the default `,`, it will add that character in between elements.

- `data`: Multidimensional list of data for each line.
- `labels`: List of labels for each row (optional).
- `filename`: Name of file.
- `char_separator`: Character separator (optional).

## Example Usage

```python
from textscribe import scribe

# Example 1: Writing to a CSV file with labels
labels = ['Name', 'Age', 'City']
data = [['John', 25, 'New York'], ['Jane', 30, 'Los Angeles']]
filename = 'example.csv'
scribe.write_to_csv(data, filename, labels=labels)

# Example 2: Writing to a TXT file with labels and a custom separator
labels = ['Name', 'Age', 'City']
data = [['John', 25, 'New York'], ['Jane', 30, 'Los Angeles']]
filename = 'example.txt'
scribe.write_to_txt(data, filename, labels=labels, char_separator='/')
```

## extract_data_by_label_csv

This function extracts data from a CSV file under a specified label.

def extract_data_by_label_csv(file_name, label):


### Args

- file_name (str): The name of the CSV file to read.
- label (str): The label to look for in the CSV file.

### Returns

- list: A list containing all the data under the given label.

### Raises

- ValueError: If the label is not found in the CSV file.
- Exception: If the file name is not a .csv file.

## extract_data_by_label_txt

This function extracts data from a TXT file under a specified label.

def extract_data_by_label_txt(file_name, label, delimiter=','):



### Args

- file_name (str): The name of the TXT file to read.
- label (str): The label to look for in the TXT file.
- delimiter (str): The character used to separate elements in the TXT file. Default is ','.

### Returns

- list: A list containing all the data under the given label.

### Raises

- ValueError: If the label is not found in the TXT file.
- Exception: If the file name is not a .txt file.

