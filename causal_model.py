import dowhy
from dowhy import CausalModel
import matplotlib.pyplot as plt

def run_dowhy_analysis(df):
    # 1. Create a Causal Model
    # Treatment: treatment, Outcome: EGFR
    # Common causes: Gene_A, batch
    model = CausalModel(
        data=df,
        treatment='treatment',
        outcome='EGFR',
        common_causes=['Gene_A', 'batch']
    )
    
    # 2. Identify Causal Effect
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
    
    # 3. Estimate the causal effect using Linear Regression
    estimate = model.estimate_effect(identified_estimand,
                                    method_name="backdoor.linear_regression")
    
    print(f"Causal Estimate: {estimate.value}")
    
    # 4. Refute the estimate
    # Placebo Treatment Refuter
    refutation = model.refute_estimate(identified_estimand, estimate, 
                                      method_name="placebo_treatment_refuter")
    print(refutation)
    
    return model, estimate
