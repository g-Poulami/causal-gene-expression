import pandas as pd
import numpy as np

def load_simulated_rna_seq():
    '''
    Generates a synthetic dataset for demonstration.
    In a real scenario, this would load a CSV or GEO dataset.
    '''
    np.random.seed(42)
    n_samples = 200
    
    # Confounders: Batch effect and Cell Cycle phase
    batch = np.random.binomial(1, 0.5, n_samples)
    cell_cycle = np.random.normal(0, 1, n_samples)
    
    # Treatment: Random assignment (simulating a randomized experiment)
    treatment = np.random.binomial(1, 0.5, n_samples)
    
    # Gene expression for Gene_A (influences the target)
    gene_a = 5 + 0.5 * cell_cycle + np.random.normal(0, 0.1, n_samples)
    
    # Target Gene (EGFR) expression
    # Causal effect of treatment is +2.0
    # Influenced by treatment, Gene_A, and Batch
    egfr = (10 + 
            2.0 * treatment + 
            1.2 * gene_a + 
            0.8 * batch + 
            np.random.normal(0, 0.5, n_samples))
            
    df = pd.DataFrame({
        'treatment': treatment,
        'EGFR': egfr,
        'Gene_A': gene_a,
        'batch': batch,
        'cell_cycle': cell_cycle
    })
    return df
