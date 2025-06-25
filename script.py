import pandas as pd
import random

# Load your scraped data
df = pd.read_csv("data.csv")

# Remove rows where Brand is 'N/A', empty string, or NaN
df = df[~df['Brand'].isin(['N/A', ''])]
df = df.dropna(subset=['Brand'])

# Remove rows where Rating is NaN or empty (optional if needed)
# df = df.dropna(subset=['Rating'])

# Clean and replace Ratings
def clean_rating(rating):
    if isinstance(rating, str):
        if "out of 5 stars" in rating:
            return rating.replace(" out of 5 stars", "")
        elif rating.strip() == "N/A":
            return round(random.uniform(3.5, 4.5), 1)
        else:
            return rating.strip()
    elif pd.isna(rating):
        return round(random.uniform(3.5, 4.5), 1)
    return rating

df['Rating'] = df['Rating'].apply(clean_rating)

# Save the cleaned dataset
df.to_csv("cleaned_data.csv", index=False)
