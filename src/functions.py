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
            "shap_wilks_norm_pval": stats.shapiro(df[col])[1],
            "normaltest_pval": stats.normaltest(df[col])[1]
            }
        ls.append(dict)

    data = pd.DataFrame(data=ls).set_index("column")

    return data


def analyze_group_differences(df, group_column, num_cols):
    # Group the data by the specified column (e.g., gender, age_bucket, etc.)
    grouped = df.groupby(group_column)
    
    # Find the minimum group size to ensure equal sampling across groups
    sample_size = min(len(group) for _, group in grouped)
    
    # Sample each group to match the minimum sample size
    sampled_groups = [group.sample(sample_size) for _, group in grouped]
    
    # Initialize results list to store test results for each numeric column
    results = []
    
    # Run Levene's and Kruskal-Wallis tests for each numerical column
    for col in num_cols:
        # Extract the values for each group
        col_values = [group[col].values for group in sampled_groups]
        
        # Perform Levene's test
        levene_statistic, levene_pvalue = stats.levene(*col_values, center='median')
        
        # Perform Kruskal-Wallis test
        kruskal_statistic, kruskal_pvalue = stats.kruskal(*col_values)
        
        # Append the results
        results.append({
            'column': col,
            'levene_statistic': levene_statistic,
            'levene_pvalue': levene_pvalue,
            'kruskal_statistic': kruskal_statistic,
            'kruskal_pvalue': kruskal_pvalue
        })
    
    return results