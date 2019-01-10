import csv
name = []
default = []
rules_global = []
rules_additional = []
with open('data/loreal-argentina-channels.csv', 'r') as file:
    r = csv.reader(file)
    for i, row in enumerate(r):
        if i>4:
            name.append(row[1])
            default.append(row[2])
            rules_global.append(row[3])
            rules_additional.append(row[5])

print([name, default, rules_global, rules_additional])
