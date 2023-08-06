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
