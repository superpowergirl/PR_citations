import pandas as pd
pr_df = pd.read_csv('aps-dataset-citations-2019.csv')
pr_number_citations = pr_df['cited_doi'].value_counts()


