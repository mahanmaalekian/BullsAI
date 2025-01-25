#for styling


import pandas as pd
df = pd.read_csv(r'data\trade_data_A_period_1.csv')  
sampled_df = df.sample(n=100, random_state=42)  
print(sampled_df)
