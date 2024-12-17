import pandas as pd

# LOAD AND EXPLORE DATA
# Reading CSV with pandas
df = pd.read_csv('C:\\Users\\jillc\\OneDrive\\Desktop\\Portfolio\\archive\\Technical Support Dataset.csv')
print("First 5 rows of the dataset:")
print(df.head())  # Display the first few rows

# Check the dataset info
print("\nDataset Information:")
print(df.info())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Get a summary of numerical columns
print("\nStatistical Summary:")
print(df.describe())

# Check column names
print("\nColumn Names:")
print(df.columns)

# DATA CLEANING
# Convert columns to datetime
date_columns = ['Created time', 'Expected SLA to resolve', 'Expected SLA to first response','First response time', 'Resolution time', 'Close time']

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Check if any duplicates exist
print("Number of duplicate rows:", df.duplicated().sum())

# Drop duplicates if any
df = df.drop_duplicates()

# Handle missing values
# Fill missing 'Agent interactions' with median value
df['Agent interactions'] = df['Agent interactions'].fillna(df['Agent interactions'].median())

# Fill missing 'Survey results' with mode
df['Survey results'] = df['Survey results'].fillna(df['Survey results'].mode()[0])

# Drop rows where 'Resolution time' or 'Close time' are missing
df = df.dropna(subset=['Resolution time', 'Close time'])

# Verify the cleaning
print("\nMissing Values after cleaning:")
print(df.isnull().sum())

# Confirm changes
print("\nCleaned Dataset Info:")
print(df.info())

# SUMMARY STATISTICS
# General Summary Stats for Numerical Columns
summary_stats = df.describe()
print("Summary Statistics for Numerical Columns:")
print(summary_stats)

# Value counts for categorical columns
categorical_cols = ['Priority', 'Status', 'Source', 'Product group', 'Support Level', 'Country']
for col in categorical_cols:
    print(f"\nValue Counts for '{col}':")
    print(df[col].value_counts())

# BUSINESS QUESTION ONE: Average Resolution Time by Priority
# Calculate resolution time in hours
df['Resolution Duration (hrs)'] = (df['Resolution time'] - df['Created time']).dt.total_seconds() / 3600

# Group by priority and calculate mean resolution time
avg_resolution_by_priority = df.groupby('Priority')['Resolution Duration (hrs)'].mean().reset_index()

# Display results
print("Average Resolution Time (in hours) by Priority:")
print(avg_resolution_by_priority)

# Visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.bar(avg_resolution_by_priority['Priority'], avg_resolution_by_priority['Resolution Duration (hrs)'], color='skyblue')
plt.title('Average Resolution Time by Priority')
plt.xlabel('Priority')
plt.ylabel('Average Resolution Time (Hours)')
plt.show()

# BUSINESS QUESTION TWO: Top Agent by Customer Satisfaction
# Group by agent and calculate mean survey results
top_agents_by_satisfaction = df.groupby('Agent Name')['Survey results'].mean().reset_index()

# Sort to find top-performing agents
top_agents_by_satisfaction = top_agents_by_satisfaction.sort_values(by='Survey results', ascending=False)

# Display top 5 agents
print("Top 5 Agents by Average Customer Satisfaction:")
print(top_agents_by_satisfaction.head())

# Visualization
plt.figure(figsize=(10, 6))
plt.bar(top_agents_by_satisfaction['Agent Name'].head(5), top_agents_by_satisfaction['Survey results'].head(5), color='green')
plt.title('Top 5 Agents by Customer Satisfaction')
plt.xlabel('Agent Name')
plt.ylabel('Average Survey Result')
plt.xticks(rotation=45)
plt.show()

# BUSINESS QUESTION THREE: Relationship Between Agent Interactions and Survey Results
import seaborn as sns

# Scatter plot to observe relationship
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Agent interactions', y='Survey results', data=df, color='purple')
plt.title('Relationship Between Agent Interactions and Survey Results')
plt.xlabel('Number of Agent Interactions')
plt.ylabel('Survey Results')
plt.show()

# Calculate correlation
correlation = df['Agent interactions'].corr(df['Survey results'])
print(f"Correlation between Agent Interactions and Survey Results: {correlation:.2f}")
