import csv

with open('growth_good_buys.csv') as f:
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    data = data[1:]
filtered_data = []
for row in data:
    all_positive = True
    for point in row[1:]:
        if float(point) == 0 or float(point) < 0 or float(point) > 300:
            all_positive = False
    if all_positive and int(row[-1]) == 5:
        filtered_data.append(row)

final_data = []
for row in filtered_data:
    new_row = [row[0]]
    for value in row[1:]:
        value = float(value)
        new_row.append(round(value, 3))
    final_data.append(new_row)


with open('./final_data/growth_good_buys_filtered.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Symbol', 'Final Weighted Rating', 'GPM', 'ROA', 'ROE', 'Gross Profit Growth', 'Net Income Growth', 'EPS Growth', 'Unweighted Rating'])
    writer.writerows(final_data)