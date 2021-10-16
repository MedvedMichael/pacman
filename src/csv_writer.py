import csv

def csv_write(filename, row):
    with open(filename, 'a') as f:
        f.write(','.join(row) + '\n')