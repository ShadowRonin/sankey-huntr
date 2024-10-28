
import os
import csv


dir = os.path.dirname(os.path.realpath('__file__'))

def csvToDict(filename):
    fields = []
    rows = []

    absoluteFilename = os.path.join(dir, filename)
    
    with open(absoluteFilename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)


    # printing the field names
    print('Field names are:' + ', '.join(field for field in fields))

    # printing first 5 rows
    print('\nFirst 5 rows are:\n')
    for row in rows[:5]:
        # parsing each column of a row
        for col in row:
            print("%10s" % col, end=" "),
        print('\n')

    objs = []
    for row in rows:
        obj = {}
        for j, field in enumerate(fields):
            if j < len(rows):
                obj[field] = row[j]
            else:
                obj[field] = ""
        objs.append(obj)

    return objs
