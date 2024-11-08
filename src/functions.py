import pandas as pd
import numpy as np
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
            "shap_wilks_norm_pval": stats.shapiro(df[col])[1],
            "normaltest_pval": stats.normaltest(df[col])[1]
            }
        ls.append(dict)

    data = pd.DataFrame(data=ls).set_index("column")

    return data


def kruskal_analysis(df, group_column, num_cols):
    # Group the data by the specified column (e.g., gender, age_bucket, etc.)
    grouped = df.groupby(group_column, observed=True)
    
    # Sample each group to match the minimum sample size
    groups = [group for _, group in grouped]
    
    # Initialize results list to store test results for each numeric column
    results = []
    
    # Run Levene's and Kruskal-Wallis tests for each numerical column
    for col in num_cols:

        if col != group_column:
            # Extract the values for each group
            col_values = [group[col].values for group in groups]
            
            # Perform Kruskal-Wallis test
            kruskal_statistic, kruskal_pvalue = stats.kruskal(*col_values)
            
            # Append the results
            results.append({
                'group_column': group_column,
                'column': col,
                'kruskal_statistic': kruskal_statistic,
                'kruskal_pvalue': kruskal_pvalue
            })
    
    return results


def leven_analysis(df, group_column, num_cols):
    # Group the data by the specified column (e.g., gender, age_bucket, etc.)
    grouped = df.groupby(group_column, observed=True)
    
    # Find the minimum group size to ensure equal sampling across groups
    sample_size = min(len(group) for _, group in grouped)
    
    # Sample each group to match the minimum sample size
    sampled_groups = [group.sample(sample_size) for _, group in grouped]
    
    # Initialize results list to store test results for each numeric column
    results = []
    
    # Run Levene's and Kruskal-Wallis tests for each numerical column
    for col in num_cols:

        if col != group_column:
            # Extract the values for each group
            col_values = [group[col].values for group in sampled_groups]
            
            # Perform Levene's test
            levene_statistic, levene_pvalue = stats.levene(*col_values, center='median')
            
            # Append the results
            results.append({
                'group_column': group_column,
                'column': col,
                'levene_statistic': levene_statistic,
                'levene_pvalue': levene_pvalue
            })
    
    return results


def chi2_test(target, features):
    """
    This function uses the chi2_contingency() statistical test to test for associations between
    categorical variables. The Cramer's V test is then used to measure the strength of the association.

    Args:
        target: The variable to be tested againsts all other categorical variables.
        features: The categorical variables.

    Returns:
        df = A dataframe showing the results of the chi2 and cramers_v tests.
    """

    if features.select_dtypes(include=['number']).empty:

        result_list = []

        for col in features.columns:

            if col != target.name:
        
                # Calculate correlations between categorical columns
                confusion_matrix = pd.crosstab(target, features[col])
                #print(confusion_matrix)
                
                # Chi-square test of independence
                chi2, p, dof, expected = stats.chi2_contingency(confusion_matrix)
                #print(chi2)
                
                # Use scientific notation for p-value if it's very small
                p_formatted = np.format_float_scientific(p, precision=2)
                
                # Calculate Cramer's V
                n = confusion_matrix.sum().sum()
                phi2 = chi2 / n
                r, k = confusion_matrix.shape
                cramers_v = np.sqrt(phi2 / min(k-1, r-1))
                
                # Interpretation of Cramér's V
                if cramers_v < 0.1:
                    interpretation = "Very weak association"
                elif cramers_v < 0.2:
                    interpretation = "Weak association"
                elif cramers_v < 0.4:
                    interpretation = "Moderate association"
                elif cramers_v < 0.6:
                    interpretation = "Relatively strong association"
                elif cramers_v < 0.8:
                    interpretation = "Strong association"
                else:
                    interpretation = "Very strong association"
                
                result_list.append({
                    "column": col,
                    "chi2_statistic": chi2,
                    "p_value": p_formatted,
                    "cramers_v": cramers_v,
                    "interpretation": interpretation
                })

        return pd.DataFrame(result_list)

    else:
        return "This features is only meant for use with categorical variables, but numerical were passed."