import os
import csv
import numpy as np
from numpy.core.fromnumeric import round_

# COPY RELATIVE FILEPATH 
csvpath = "Resources\\election_data.csv"

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
        all_rows.append(row)

# DO NOT print (all_rows)... too much data

total_votes = len(all_rows)

votes = {}

for row in all_rows:
    candidate = row[2]
    if candidate in votes.keys():
        votes[candidate] += 1
    else:
        votes[candidate] = 1
print(votes)

winning_politician = ""
init_votes = 0
for politician in votes.keys():
    votes_won = votes[politician]
    if votes_won > init_votes:
        init_votes = votes_won
        winning_politician = politician

print("Election Results\n")
print("----------------------------\n")
print("Total Votes: {total_votes\n")
print("-------------------------\n")
print("-------------------------\n")
print("Winner: {winning_politician)\n")
print("-------------------------")

out_path = "pypollhmwk.txt"
with open(out_path, "w") as f:
    f.write(f"Election Results\n")
    f.write(f"-------------------------\n")
    f.write(f"Total Votes: {total_votes}\n")
    f.write(f"-------------------------\n")

    for politician in votes.keys():
        f.write(f"{politician}: {round(votes[politician]/total_votes * 100)}% ({votes[politician]}\n")

    f.write(f"-------------------------\n")
    f.write(f"Winner: {winning_politician}\n")
    f.write(f"-------------------------\n")
   
    


