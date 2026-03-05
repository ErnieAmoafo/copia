import os
import pandas as pd
from copia.estimators import diversity 
from copia.data import to_copia_dataset


if __name__ == '__main__':
    # Load via path to data
    data_path = os.path.join('datasets', 'abundance.csv')
    print(f"Loading data from {data_path}...")

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Could not find the file at {data_path}.")
        exit()

    counts = df['count'].values
    dataset = to_copia_dataset(counts, data_type='abundance', input_type='counts')

    print(f"Data loaded successfully. Observed Editions (Species): {dataset.S_obs}")
    print("Running Zero-Truncated Negative Binomial estimation with 100 bootstrap iterations...")

    try:
        results = diversity(
            dataset, 
            method='ztnb', 
            CI=True, 
            n_iter=100
        )

        print("\n--- Raw Copia Output ---")
        print(results)

        print("\n--- Zero-Truncated Negative Binomial Estimation Results ---")
        print(f"Observed Editions: {dataset.S_obs}")
        
        # Safely extract using 'est'
        est_total = results['est']
        lci = results['lci']
        uci = results['uci']
        
        print(f"Estimated Total Heritage (Observed + Lost): {est_total:.2f}")
        
        estimated_lost = est_total - dataset.S_obs
        print(f"Estimated Lost Editions (Dark Matter): {estimated_lost:.2f}")
        print(f"95% Confidence Interval for Total: [{lci:.2f}, {uci:.2f}]")

    except Exception as e:
        print(f"\nAn error occurred: {e}")