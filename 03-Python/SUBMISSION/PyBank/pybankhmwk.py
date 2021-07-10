import os
import csv
import numpy as np

# COPY RELATIVE FILEPATH 
csvpath = "Resources\\budget_data.csv"

# Read in the CSV data- row by row to form list of list
with open(csvpath) as csvfile:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    print(f"CSV Header: {csv_header}")
 
    # store all my rows as a list of lists
    all_rows = []
    for row in csvreader:
        clean_row = row
        clean_row[1] = int(clean_row[1])
        all_rows.append(clean_row)
print (all_rows)

total_months = (len(all_rows))
print (total_months)

total_profits = [x[1] for x in all_rows]
sum_profit = sum(total_profits)
print (sum(total_profits))

diff = []
for i in range(len(all_rows) -1):
    curr_profit = all_rows[i][1]
    next_profit = all_rows[i + 1][1]   

    difference = next_profit - curr_profit
    diff.append(difference)
 
average_diff = np.mean(diff) 
print (average_diff)

max_difference = max(diff)
min_difference = min(diff)

print (max_difference)
print (min_difference)

max_difference_indx = diff.index(max_difference) + 1
max_month = all_rows[max_difference_indx][0]
print (max_month)

min_difference_indx = diff.index(min_difference) + 1
min_month = all_rows[min_difference_indx][0]
print (min_month)

print("Financial Analysis\n")
print("----------------------------\n")
print("Total Months: {total_months\n")
print("Total: ${sum_profit\n")
print("Average Change: ${round(average_diff, 2)\n")
print("Greatest Increase in Profits: {max_month (${max_difference})\n")
print("Greatest Decrease in Profits: {min_month (${min_difference})")

out_path = "pybankhmwk.txt"
with open(out_path, "w") as f:
    f.write(f"Financial Analysis\n")
    f.write(f"----------------------------\n")
    f.write(f"Total Months: {total_months}\n")
    f.write(f"Total: ${sum_profit}\n")
    f.write(f"Average Change: ${round(average_diff, 2)}\n")
    f.write(f"Greatest Increase in Profits: {max_month} (${max_difference})\n")
    f.write(f"Greatest Decrease in Profits: {min_month} (${min_difference})")
