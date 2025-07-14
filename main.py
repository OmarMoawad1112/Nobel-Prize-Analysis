# Import necessary libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the Nobel Prize dataset
nobel_df = pd.read_csv('data/nobel.csv')


# Create a new column for the decade (e.g., 1990, 2000, etc.)
nobel_df['decade'] = (nobel_df['year'] // 10) * 10

# Count the number of winners by gender
sex_frequencies = nobel_df['sex'].value_counts()

# Count the number of winners by birth country
country_frequencies = nobel_df['birth_country'].value_counts()

# Get the top 3 countries by number of Nobel winners
top_3_countries = country_frequencies.index[:3]

# Create a new DataFrame with only winners from the top 3 countries
top_countries_df = nobel_df[nobel_df['birth_country'].isin(top_3_countries)]

# Store the most common gender and birth country
top_gender = sex_frequencies.index[0]
top_country = country_frequencies.index[0]

# Create a new DataFrame to analyze US winner ratios by decade
decade_counts = pd.DataFrame()
# Count number of US-born winners per decade
decade_counts['USA Winners'] = nobel_df[nobel_df['birth_country'] == 'United States of America'].groupby('decade').size()
# Count total winners per decade
decade_counts['Total Winners'] = nobel_df.groupby('decade').size()
# Compute the ratio of US winners to total winners
decade_counts['Ratio'] = decade_counts['USA Winners'] / decade_counts['Total Winners']
# Sort the decades by ratio in descending order
decade_counts.sort_values('Ratio' , ascending=False, inplace=True)

# Get the decade with the highest US-winner ratio
max_decade_usa = decade_counts.index[0]





# Initialize an empty dictionary to store the result
max_female_dict = dict()
decade_winners = pd.DataFrame()

# Group by decade and category, count total winners in each group
decade_winners['Total Winners'] = nobel_df.groupby(['decade', 'category']).size()

# Group by decade and category, count number of female winners in each group
decade_winners['Female Winners'] = nobel_df[nobel_df['sex'] == 'Female'].groupby(['decade', 'category']).size()

# Replace NaN values in Female Winners with 0 (i.e., no females in that group)
decade_winners.fillna(0, inplace=True)

# Calculate the ratio (proportion) of female winners in each group
decade_winners['Ratio'] = decade_winners['Female Winners'] / decade_winners['Total Winners']
decade_winners.sort_values('Ratio', ascending=False, inplace=True)

# Get the decade and category for the top row (highest female winner ratio)
decade, category = decade_winners.index[0]
decade = int(decade)

# Store the result in the dictionary in the required format {decade: category}
max_female_dict[decade] = category


# Filter out only the female winners and keep relevant columns
females_df = nobel_df[nobel_df['sex'] == 'Female'][['year','full_name' , 'category']]
# Get the first woman to win a Nobel Prize
first_woman_name = females_df.iloc[0,1]
first_woman_category = females_df.iloc[0,2]

# Count repeat individuals
repeated_individuals = nobel_df['full_name'].value_counts()
repeated_individuals = repeated_individuals[repeated_individuals >= 2]
individual_names = repeated_individuals.index.tolist()

# Combine into one repeat list
repeat_list = individual_names

# ---------------------- PLOTS -----------------------

sns.set_style('darkgrid')
sns.set_context('notebook')

# Plot gender distribution
sns.catplot(kind='count', x='sex', data=nobel_df, hue='sex')
plt.ylabel("Number of Winners")
plt.title("Distribution of Nobel Prizes by Gender")
plt.yticks(sex_frequencies.values)  # Set tick values to actual counts
plt.tight_layout()
plt.savefig('reports/Nobel Prizes by Gender.png')
plt.show()

# Plot country distribution for top 3 countries
sns.catplot(kind='count', x='birth_country', data=top_countries_df,
            hue='birth_country', order=['Germany', 'United Kingdom', 'United States of America'])
plt.yticks(country_frequencies[:3].values)
plt.xlabel("Country")
plt.ylabel("Number of Nobel Prize Winners")
plt.title("Top 3 Countries by Number of Nobel Prize Winners")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/Top 3 Nobel Prize Winners Countries.png')
plt.show()

# Plot ratio of US-born winners by decade
sns.catplot(kind='bar', x='decade', y='Ratio', data=decade_counts,
            hue='decade', legend=False)
plt.xticks(rotation=90)
plt.ylabel("Ratio of US-born Winners")
plt.title("Ratio of US-born Nobel Prize Winners per Decade")
plt.tight_layout()
plt.savefig('reports/US-Born Nobel Prize Winners per Decade.png')
plt.show()
