# Counterfactual Gene Expression Analysis with CausalPy & DoWhy

![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![Build Status](https://github.com/g-Poulami/causal-gene-expression/actions/workflows/python-app.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Bioinformatics](https://img.shields.io/badge/domain-Bioinformatics-orange.svg)

## Project Overview
This project addresses a critical gap in transcriptomic analysis: distinguishing between correlation and causation. While standard differential expression (DE) can identify genes that change in response to a drug, it often picks up noise from batch effects or secondary biological processes. 

Using a causal inference framework, we ask the counterfactual question: "What would the EGFR expression in these specific treated samples have been if they had not received the treatment?"

## The Biological Question
Does Drug X causally regulate EGFR expression, or is the observed shift mediated by sequencing batch effects or co-expression with Gene_A?

To solve this, we modeled the relationship between:
- **Treatment**: Binary exposure to Drug X.
- **Outcome**: EGFR expression levels (Normalized).
- **Confounders**: Batch ID (technical variance) and Gene_A (a proxy for a shared regulatory pathway).

## Key Visualizations & Technical Interpretations

### 1. Causal Directed Acyclic Graph (DAG)
The DAG represents our structural assumptions about the data-generating process. 

![Causal DAG](causal_dag.png)

*   **Logic**: We explicitly defined **Batch** and **Gene_A** as "common causes" (confounders).
*   **Significance**: By mapping these paths, the DoWhy library identifies the "Backdoor Criterion," allowing us to block the influence of non-treatment variables and isolate the true causal effect of the drug on EGFR.

### 2. Counterfactual Impact Distribution
This density plot represents the estimated causal effect using a Bayesian approach.

![Counterfactual Plot](counterfactual_plot.png)

*   **Observed (Teal)**: The actual measured expression of EGFR in the treated cell lines.
*   **Counterfactual (Orange)**: The model's prediction of what those same treated cells would look like without the drug.
*   **Interpretation**: The clear shift between the peaks quantifies the ~1.91 units of expression directly attributable to the drug treatment, rather than noise or confounding.

## Model Robustness & Refutation
A causal estimate is only valid if it survives "attacks" on its logic. This model was subjected to a Placebo Treatment Refutation:
- **Test**: The real treatment was replaced with random noise.
- **Result**: The estimated effect dropped from 1.91 to near zero (~ -0.01).
- **Validation**: A p-value of 1.0 confirms that the placebo had no effect, strongly supporting the validity of our original 1.91 estimate.

## Tech Stack
- **Python**
- **DoWhy**: Causal model identification and robustness testing.
- **CausalPy / PyMC**: Bayesian counterfactual estimation.
- **NetworkX**: Graph structure representation.
- **Seaborn**: Data visualization.
- **GitHub Actions**: Continuous Integration.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute the pipeline:
   ```bash
   python main.py
   ```
