import csv
import os

def save_to_csv(data, filename="data/products.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

