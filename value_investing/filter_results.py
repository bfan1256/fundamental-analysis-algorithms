import csv

with open('undervalued_good_buys.csv') as f:
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    data = data[1:]
filtered_data = []
for row in data:
    if float(row[1]) <= 6 and float(row[-3]) < 1:
        filtered_data.append(row)

final_data = []
for row in filtered_data:
    new_row = [row[0]]
    for value in row[1:]:
        value = float(value)
        new_row.append(round(value, 3))
    final_data.append(new_row)


with open('./final_data/undervalued_good_buys_filtered.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Symbol', 'Final Weighted Rating', 'DCF/P', 'PEG', 'Dividend Payout Ratio', 'P/FV', 'Unweighted Rating'])
    writer.writerows(final_data)