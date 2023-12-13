import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv("DS1_C5_S3_BazilHousing_Data_Hackathon.csv") 

# Display basic information about the dataset
print(data.info())
print(data.head())

# Data Preprocessing
data.dropna(inplace=True)

# Convert categorical variables into numerical format
data['animal'] = data['animal'].map({'acept': 1, 'not acept': 0})
data['furniture'] = data['furniture'].map({'furnished': 1, 'not furnished': 0})

# Define criteria for different household types
bachelor_criteria = {'rooms': 1, 'bathroom': 1, 'parking spaces': 1}
mid_size_family_criteria = {'rooms': 3, 'bathroom': 2, 'parking spaces': 1}
large_family_criteria = {'rooms': 4, 'bathroom': 3, 'parking spaces': 2}

# Create subsets of data for each household type
bachelor_data = data[(data['rooms'] >= bachelor_criteria['rooms']) &
                     (data['bathroom'] >= bachelor_criteria['bathroom']) &
                     (data['parking spaces'] >= bachelor_criteria['parking spaces'])]

mid_size_family_data = data[(data['rooms'] >= mid_size_family_criteria['rooms']) &
                            (data['bathroom'] >= mid_size_family_criteria['bathroom']) &
                            (data['parking spaces'] >= mid_size_family_criteria['parking spaces'])]

large_family_data = data[(data['rooms'] >= large_family_criteria['rooms']) &
                         (data['bathroom'] >= large_family_criteria['bathroom']) &
                         (data['parking spaces'] >= large_family_criteria['parking spaces'])]

# Calculate a suitability score for each city based on selected features
def calculate_suitability_score(data_subset):
    score = data_subset['rent amount (R$)'] + data_subset['parking spaces'] + data_subset['furniture']
    return score

bachelor_data['Suitability_score'] = calculate_suitability_score(bachelor_data)
mid_size_family_data['Suitability_score'] = calculate_suitability_score(mid_size_family_data)
large_family_data['Suitability_score'] = calculate_suitability_score(large_family_data)

# Recommend top cities for each household type
def recommend_cities(data_subset, num_recommendations):
    top_cities = data_subset.nsmallest(num_recommendations, 'Suitability_score')
    return top_cities

bachelor_recommendations = recommend_cities(bachelor_data, num_recommendations=5)
mid_size_family_recommendations = recommend_cities(mid_size_family_data, num_recommendations=5)
large_family_recommendations = recommend_cities(large_family_data, num_recommendations=5)

# Visualization using Matplotlib
plt.figure(figsize=(12, 6))

# Bachelor Recommendations
plt.subplot(131)
plt.bar(bachelor_recommendations['city'], bachelor_recommendations['Suitability_score'])
plt.title("Bachelor Recommendations")
plt.xticks(rotation=45)

# Mid-Size Family Recommendations
plt.subplot(132)
plt.bar(mid_size_family_recommendations['city'], mid_size_family_recommendations['Suitability_score'])
plt.title("Mid-Size Family Recommendations")
plt.xticks(rotation=45)

# Large Family Recommendations
plt.subplot(133)
plt.bar(large_family_recommendations['city'], large_family_recommendations['Suitability_score'])
plt.title("Large Family Recommendations")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
