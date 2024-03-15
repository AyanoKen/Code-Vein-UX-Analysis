import csv
import re

# Open the text files
with open('Recommended.txt', 'r', encoding='utf-8') as file1, \
     open('hours.txt', 'r', encoding='utf-8') as file2, \
     open('Reviews.txt', 'r', encoding='utf-8') as file3:

    # Read the content of each file and split into items
    content1 = file1.read().splitlines()
    content2 = file2.read().splitlines()
    content3 = file3.read().splitlines()

for content in content3:
    content = re.sub(r'\s+', ' ', content)

filtered_content3 = [s for s in content3 if any(c.isalpha() for c in s) or s.isdigit()]

# Combine the contents into a list of tuples
combined_content = zip(content1, content2, filtered_content3)

# Write the combined content to a CSV file
with open('output.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Column1', 'Column2', 'Column3'])  # Header row
    writer.writerows(combined_content)