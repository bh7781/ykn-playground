import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

def calculate_cramers_v(df, col1, col2):
    contingency_table = pd.crosstab(df[col1], df[col2])

    chi2, _, _, _ = chi2_contingency(contingency_table)

    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))    
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    cramers_v = np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

    return cramers_v

def cramers_v_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = df.select_dtypes(include=['object', 'category']).columns
    corr_matrix = pd.DataFrame(index=cols, columns=cols)
    for col1 in cols:
        for col2 in cols:
            corr_matrix.at[col1, col2] = calculate_cramers_v(df, col1, col2)
    return corr_matrix

data = {
    'Advocate': ['Adv 1', 'Adv 1', 'Adv 2', 'Adv 3', 'Adv 3', 'Adv 2', 'Adv 3', 'Adv 1'],
    'Company': ['Comp A', 'Comp A', 'Comp C', 'Comp B', 'Comp B', 'Comp D', 'Comp E', 'Comp A']
}

df = pd.DataFrame(data)

print(cramers_v_matrix(df))
