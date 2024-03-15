import csv
import math

# Function to read CSV file and calculate correlation coefficient
def calculate_correlation(csv_file):
    hours_played = []
    recommendations = []

    # Read CSV file and extract data
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            hours_played.append(float(row[1].replace(',', '')))
            recommendations.append(1 if row[0] == 'Recommended' else 0)

    # Calculate means
    mean_hours = sum(hours_played) / len(hours_played)
    mean_recommendations = sum(recommendations) / len(recommendations)

    # Calculate covariance and variances
    covariance = sum((x - mean_hours) * (y - mean_recommendations) for x, y in zip(hours_played, recommendations))
    var_hours = sum((x - mean_hours) ** 2 for x in hours_played)
    var_recommendations = sum((y - mean_recommendations) ** 2 for y in recommendations)

    # Calculate correlation coefficient

    print("Covariance is: " + str(covariance))
    print("var_hours is: " + str(var_hours))
    print("var_recommendations is : " + str(var_recommendations))

    correlation = covariance / math.sqrt(var_hours * var_recommendations)

    return correlation

correlation = calculate_correlation("output.csv")

print(correlation)
