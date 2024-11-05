import pandas as pd
from scipy import stats

def shape(df, alt="two-sided"):
    """
    This function tests the null hypothesis that the skewness and kurtosis of the population
    from which the sample was drawn is that of the normal distribution.

    Args:
        df = dataframe with only numerical columns
        alt = defines the alternative hypothesis ('two-sided', 'less' , 'greater')
        
    Returns:
        shape_df = a dataframe containing the results of the tests
    """
    ls = []
    for col in df.columns:
        dict = {
            "column": col,
            "skew": stats.skew(df[col]),
            "skew_pval": stats.skewtest(df[col], alternative=alt)[1],
            "kurtosis": stats.kurtosis(df[col]),
            "kurt_pval": stats.kurtosistest(df[col], alternative=alt)[1],
            "shap_wilks_norm_pval": stats.shapiro(df[col])[1]
            }
        ls.append(dict)

    data = pd.DataFrame(data=ls).set_index("column")

    return data