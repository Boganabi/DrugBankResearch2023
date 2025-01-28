import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv('../csv-files/approvedInnerProducts.csv')

approvedRaw = pd.read_csv('../csv-files/drugbank05_drugs.csv')
approvedRaw = approvedRaw[approvedRaw["approved"] == 1] # drops values that dont have 1 for approved

approvedRaw.head()

# comment out if we dont want to filter by approved data
data = data[data["drug ID 1"].isin(approvedRaw["drugbank_id"])]

# Display the first few rows of the data
data.head()

# Number of unique drugs in the dataset
unique_drugs = set(data['drug ID 1']).union(set(data['drug ID 2']))
num_unique_drugs = len(unique_drugs)

# Distribution of the similarity column
similarity_distribution = data['similarity'].value_counts(normalize=True)

# Number of unique drug pairs
num_unique_pairs = len(data)

num_unique_drugs, similarity_distribution, num_unique_pairs

# Setting the style for the visualizations
sns.set_style("whitegrid")

# Plotting the distribution of similarity values
def plotSimDist():
    plt.figure(figsize=(8, 6))
    sns.countplot(data=data, x='similarity')
    plt.title("Distribution of Similarity Values")
    plt.show()

# Filtering only the drug pairs with similarity = 1
similar_pairs = data[data['similarity'] == 1]

# Counting the number of similar drugs for each drug in 'drug ID 1'
similar_counts = similar_pairs['drug ID 1'].value_counts().head(10)

# Plotting the top drugs with the most similar pairs
def plotMostSimilar():
    plt.figure(figsize=(12, 8))
    sns.barplot(y=similar_counts.index, x=similar_counts.values, palette="viridis")
    plt.title("Top Drugs with the Most Similar Pairs")
    plt.xlabel("Count of Similar Drug Pairs")
    plt.ylabel("Drug ID")
    plt.show()

# Top 10 most common similarity scores
def plotMostCommon():
    top_10_scores = similarity_distribution.head(10)

    plt.figure(figsize=(10, 6))
    top_10_scores.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Top 10 Most Common Similarity Scores')
    plt.xlabel('Similarity Score')
    plt.ylabel('Proportion of Drug Pairs')
    plt.grid(axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

# Convert drug IDs to numeric values
def plotScatter():
    data['drug ID 1 numeric'] = data['drug ID 1'].str.replace('DB', '').astype(int)
    data['drug ID 2 numeric'] = data['drug ID 2'].str.replace('DB', '').astype(int)

    # Scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(data['drug ID 1 numeric'], data['similarity'], alpha=0.5, label='Drug ID 1')
    plt.scatter(data['drug ID 2 numeric'], data['similarity'], alpha=0.5, label='Drug ID 2', color='red')
    plt.title('Scatter Plot of Drug IDs vs. Similarity Scores')
    plt.xlabel('Drug ID (Numeric Value)')
    plt.ylabel('Similarity Score')
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Box plot for similarity scores
def plotSimilarities():
    data['drug ID 1 numeric'] = data['drug ID 1'].str.replace('DB', '').astype(int)
    data['drug ID 2 numeric'] = data['drug ID 2'].str.replace('DB', '').astype(int)

    plt.figure(figsize=(10, 6))
    sns.boxplot(y=data['similarity'])
    plt.title('Box Plot of Similarity Scores')
    plt.ylabel('Similarity Score')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def plotDescriptionSimilarities():
    plt.figure(figsize=(10, 6))
    # bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    plt.hist(data["description_similarity"], bins=30, edgecolor="k")
    # plt.xticks(bins)

    plt.title("Distribution of Similarities in Drug Descriptions")
    plt.xlabel("Similarity Rating")
    plt.ylabel("Count")

    plt.show()

plotDescriptionSimilarities()