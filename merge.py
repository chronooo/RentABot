import csv

# Read the first CSV file
file1 = "Bobaholics - 2023 All Data.csv"
file2 = "members_with_specific_role.csv"
output_file = "merged_file.csv"

with open(file1, "r", newline="") as f1, open(file2, "r", newline="") as f2:
    # Create CSV readers for both files
    reader1 = csv.reader(f1)
    reader2 = csv.reader(f2)

    # Create a CSV writer for the output file
    with open(output_file, "w", newline="") as output_f:
        writer = csv.writer(output_f)

        # Read the headers from both files
        headers1 = next(reader1)
        headers2 = next(reader2)

        # Find the index of the "Discord" and "UserID" columns in each file
        discord_index1 = headers1.index("Discord")
        username_index2 = headers2.index("Username")
        userid_index2 = headers2.index("UserID")

        # Modify the header order to place "UserID" as the second column
        headers1.insert(1, "UserID")
        writer.writerow(headers1)

        # Create a dictionary to store the UserID values
        user_id_dict = {row[username_index2]: row[userid_index2] for row in reader2 if row[userid_index2]}

        # Merge the data based on the "Discord" matching "Username"
        for row1 in reader1:
            discord_value = row1[discord_index1]
            user_id = user_id_dict.get(discord_value, "")
            row1.insert(1, user_id)
            writer.writerow(row1)

print("Merged file saved as", output_file)