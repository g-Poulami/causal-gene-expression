import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from data_loader import load_simulated_rna_seq
from causal_model import run_dowhy_analysis

def generate_visuals(df, model, estimate):
    # 1. Manually Draw the DAG using NetworkX to avoid blank files
    print("Generating DAG diagram...")
    plt.figure(figsize=(8, 6))
    
    # Create a manual graph to match your model structure
    G = nx.DiGraph()
    G.add_edges_from([
        ('batch', 'treatment'),
        ('batch', 'EGFR'),
        ('Gene_A', 'treatment'),
        ('Gene_A', 'EGFR'),
        ('treatment', 'EGFR')
    ])
    
    pos = {'batch': (0, 1), 'Gene_A': (0, -1), 'treatment': (1, 0), 'EGFR': (2, 0)}
    
    nx.draw_networkx(
        G, pos, with_labels=True, node_color='skyblue', 
        node_size=3000, font_size=10, font_weight='bold', 
        arrowsize=20, edge_color='gray'
    )
    
    plt.title("Causal DAG: Identified Confounders & Treatment Path")
    plt.axis('off')
    plt.savefig("causal_dag.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Successfully saved: causal_dag.png")

    # 2. Re-save Counterfactual Plot[cite: 3]
    print("Generating Counterfactual distribution...")
    plt.figure(figsize=(10, 6))
    treated_df = df[df['treatment'] == 1]
    observed_treated = treated_df['EGFR']
    counterfactual_untreated = observed_treated - estimate.value

    sns.kdeplot(observed_treated, label="Observed (Treated)", fill=True, color="teal")
    sns.kdeplot(counterfactual_untreated, label="Counterfactual (If Untreated)", fill=True, color="orange")
    
    plt.title(f"Causal Impact on EGFR Expression (Estimate: {estimate.value:.2f})")
    plt.legend()
    plt.savefig("counterfactual_plot.png", dpi=300)
    plt.close()
    print("Successfully saved: counterfactual_plot.png")
    plt.close()

    # 2. Plot Observed vs. Counterfactual Distributions
    # Quantifies the drug effect (1.91) by comparing real vs. predicted states
    print("Generating Counterfactual distribution...")
    plt.figure(figsize=(10, 6))
    
    treated_df = df[df['treatment'] == 1]
    observed_treated = treated_df['EGFR']
    
    # Counterfactual: What expression would be if treatment was 0[cite: 3]
    counterfactual_untreated = observed_treated - estimate.value

    sns.kdeplot(observed_treated, label="Observed (Treated)", fill=True, color="teal")
    sns.kdeplot(counterfactual_untreated, label="Counterfactual (If Untreated)", fill=True, color="orange")
    
    plt.title(f"Causal Impact on EGFR Expression (Estimate: {estimate.value:.2f})")
    plt.xlabel("Expression Level (Normalized)")
    plt.ylabel("Density")
    plt.legend()
    plt.savefig("counterfactual_plot.png", dpi=300)
    plt.close()
    print("Successfully saved: counterfactual_plot.png")

def main():
    print("Loading data...")
    df = load_simulated_rna_seq()
    
    print("\nRunning DoWhy Causal Analysis...")
    # This identifies the causal effect while adjusting for Gene_A and Batch
    model, estimate = run_dowhy_analysis(df)
    
    generate_visuals(df, model, estimate)
    print("\nProject workflow complete.")

if __name__ == "__main__":
    main()