import pandas as pd
import copia
from copia.data import to_copia_dataset

# Load project data
print("Loading data from abundance.csv...")
df = pd.read_csv('abundance.csv')

# Extract the 'count' column as a numpy array
counts = df['count'].values

# Convert to copia's AbundanceData format
# We specify input_type='counts' because the CSV lists the actual observation count for each individual edition.
dataset = to_copia_dataset(counts, data_type='abundance', input_type='counts')

print(f"Data loaded successfully. Observed Editions (Species): {dataset.S_obs}")
print("Running Zero-Truncated Negative Binomial estimation with 100 bootstrap iterations...")
print("(This might take a few moments...)")

# Use Copia's diversity wrapper to run the ZTNB estimator with Bootstrap CI
try:
    results = copia.diversity(
        dataset, 
        method='ztnb', 
        CI=True, 
        n_iter=100  # Number of bootstrap iterations for the confidence interval
    )

    # Display the results
    print("\n--- Zero-Truncated Negative Binomial Estimation Results ---")
    print(f"Observed Editions: {dataset.S_obs}")
    print(f"Estimated Total Heritage (Observed + Lost): {results['richness']:.2f}")
    
    # Calculate the dark matter (f0)
    estimated_lost = results['richness'] - dataset.S_obs
    print(f"Estimated Lost Editions (Dark Matter): {estimated_lost:.2f}")
    print(f"95% Confidence Interval for Total: [{results['lci']:.2f}, {results['uci']:.2f}]")

except KeyError:
    print("\nError: The 'ztnb' method was not found.")
    print("Please make sure you added 'ztnb' to the ESTIMATORS dictionary and __all__ list at the bottom of copia/estimators.py!")