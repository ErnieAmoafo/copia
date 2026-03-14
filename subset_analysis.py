import os
import pandas as pd
from copia.estimators import diversity
from copia.data import to_copia_dataset

# Windows Multiprocessing Shield
if __name__ == '__main__':
    print("Starting Subset Analysis for Language and Format...\n")
    results_list = []

    # 1. Analyze Languages
    print("--- Analyzing Languages ---")
    lang_path = os.path.join('datasets', 'abundance-by-language.csv')
    df_lang = pd.read_csv(lang_path)
    
    for lang in df_lang['nyelv'].unique():
        print(f"Fitting ZTNB for Language: {lang.capitalize()}...")
        counts = df_lang[df_lang['nyelv'] == lang]['count'].values
        
        "CRITICAL FIX: Remove 0-counts (hypothetical books)"
        "ZTNB must only be trained on books that physically survived (count >= 1)"
        counts = counts[counts > 0] 
        
        if len(counts) == 0:
            print(f"Skipping {lang}: No surviving books found after filtering.")
            continue

        dataset = to_copia_dataset(counts, data_type='abundance', input_type='counts')
        
        try:
            res = diversity(dataset, method='ztnb', CI=True, n_iter=100)
            
            # Safely extract the estimates to prevent KeyErrors
            if hasattr(res, 'keys'):
                est_total = float(res['est']) if 'est' in res else float(res.iloc[0])
                lci = float(res['lci']) if 'lci' in res else 0.0
                uci = float(res['uci']) if 'uci' in res else 0.0
            else:
                est_total = float(res)
                lci, uci = 0.0, 0.0

            lost = est_total - dataset.S_obs
            survival_rate = (dataset.S_obs / est_total) * 100
            
            results_list.append({
                'Category': 'Language',
                'Subset': lang.capitalize(),
                'Observed': dataset.S_obs,
                'Estimated_Total': round(est_total, 2),
                'Estimated_Lost': round(lost, 2),
                'Survival_Rate_%': round(survival_rate, 2),
                'CI_Lower': round(lci, 2),
                'CI_Upper': round(uci, 2)
            })
        except Exception as e:
            print(f"Error analyzing {lang}: {type(e).__name__} - {e}")
            print(f"Raw output was: {res}")

    # 2. Analyze Formats
    print("\n--- Analyzing Formats ---")
    fmt_path = os.path.join('datasets', 'abundance-by-format.csv')
    df_format = pd.read_csv(fmt_path)
    
    for fmt in df_format['format'].unique():
        print(f"Fitting ZTNB for Format: {fmt}...")
        counts = df_format[df_format['format'] == fmt]['count'].values
        
        # CRITICAL FIX: Remove 0-counts
        counts = counts[counts > 0]
        
        if len(counts) == 0:
            print(f"Skipping {fmt}: No surviving books found after filtering.")
            continue

        dataset = to_copia_dataset(counts, data_type='abundance', input_type='counts')
        
        try:
            res = diversity(dataset, method='ztnb', CI=True, n_iter=100)
            
            # Safely extract the estimates
            if hasattr(res, 'keys'):
                est_total = float(res['est']) if 'est' in res else float(res.iloc[0])
                lci = float(res['lci']) if 'lci' in res else 0.0
                uci = float(res['uci']) if 'uci' in res else 0.0
            else:
                est_total = float(res)
                lci, uci = 0.0, 0.0

            lost = est_total - dataset.S_obs
            survival_rate = (dataset.S_obs / est_total) * 100
            
            results_list.append({
                'Category': 'Format',
                'Subset': str(fmt),
                'Observed': dataset.S_obs,
                'Estimated_Total': round(est_total, 2),
                'Estimated_Lost': round(lost, 2),
                'Survival_Rate_%': round(survival_rate, 2),
                'CI_Lower': round(lci, 2),
                'CI_Upper': round(uci, 2)
            })
        except Exception as e:
            print(f"Error analyzing format {fmt}: {type(e).__name__} - {e}")

    # 3. Create Summary Table and Save
    if results_list:
        summary_df = pd.DataFrame(results_list)
        print("\n-----------SUBSET ANALYSIS RESULTS-----------")
        print(summary_df.to_string(index=False))
        
        output_file = 'subset_analysis_results.csv'
        summary_df.to_csv(output_file, index=False)
        print(f"\nResults successfully saved to {output_file}!")
    else:
        print("\nNo results were generated. Please check for errors above.")