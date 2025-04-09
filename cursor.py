import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Read the CSV file
df = pd.read_csv(os.path.join(os.path.expanduser('~/Desktop'), 'candidate_dataset(1).csv'))

# Get row 7 and split values by semicolon
df_row_7 = df.iloc[[6]]
split_data = {col: df_row_7[col].str.split(';').iloc[0] for col in df_row_7.columns}
df_split = pd.DataFrame(split_data)

# Convert first row to integers and create multiplied row
first_row = pd.to_numeric(df_split.iloc[0], errors='coerce').fillna(0).astype(int)
df_with_multiplied = pd.concat([df_split, pd.DataFrame([first_row * 4])], ignore_index=True)

# Transpose and rename columns
df_transposed = df_with_multiplied.T
df_transposed.columns = ['Quarterly Revenue' if i == 0 else 
                        'Quarter' if i == 7 else 
                        'Implied ARR' if i == len(df_transposed.columns) - 1 else 
                        col for i, col in enumerate(df_transposed.columns)]

# Process final DataFrame
df_final = (df_transposed
            .reset_index()
            .assign(Implied_ARR=lambda x: pd.to_numeric(x['Implied ARR'], errors='coerce').astype(int))
            .assign(Quarter=lambda x: x['Quarter'].str.replace(r'(\d{4})Q', r'\1 Q', regex=True))
            .query('Implied_ARR > 0')
            [['Quarterly Revenue', 'Quarter', 'Implied ARR']]
            .reset_index(drop=True))

# Create the line plot
plt.figure(figsize=(12, 6))
plt.plot(df_final['Quarter'], df_final['Implied ARR'], marker='o', linestyle='-')

# Set y-axis to start at 0
plt.ylim(bottom=0)

# Format y-axis as currency in thousands
def currency_formatter(x, pos):
    return f'${x/1000:,.0f}'

plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_formatter))

# Add labels and title
plt.xlabel('Quarter')
plt.ylabel('Implied ARR ($K)')
plt.title('DDOG Implied ARR by Quarter')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add horizontal grid lines only
plt.grid(axis='y')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot
plt.show()

# Display the final DataFrame
print("\nFinal DataFrame after all transformations:")
print(df_final)
