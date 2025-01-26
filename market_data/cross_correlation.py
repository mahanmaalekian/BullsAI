import pandas as pd
import matplotlib.pyplot as plt


file_paths_A = [
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A1.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A2.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A3.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A4.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A5.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A6.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A7.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A8.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A9.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A10.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A11.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A12.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A13.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A14.csv',
    'Clean A Data\content\CleanMLData\A\clean_trade_data_A15.csv',
]

file_paths_B = [
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B1.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B2.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B3.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B4.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B5.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B6.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B7.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B8.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B9.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B10.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B11.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B12.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B13.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B14.csv',
    'Clean B Data\content\CleanMLData\B\clean_trade_data_B15.csv',
]


file_paths_C = [
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C1.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C2.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C3.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C4.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C5.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C6.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C7.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C8.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C9.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C10.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C11.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C12.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C13.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C14.csv',
    '\Clean C Data\content\CleanMLData\C\clean_trade_data_C15.csv',
]

file_paths_D = [
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D1.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D2.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D3.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D4.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D5.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D6.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D7.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D8.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D9.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D10.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D11.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D12.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D13.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D14.csv',
    '\Clean D Data\content\CleanMLData\D\clean_trade_data_D15.csv',
]

file_paths_E = [
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E1.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E2.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E3.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E4.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E5.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E6.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E7.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E8.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E9.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E10.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E11.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E12.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E13.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E14.csv',
    '.\Clean E Data\content\CleanMLData\E\clean_trade_data_E15.csv',
]



def compute_cross_correlation(dataframe1, dataframe2, lag_range=(-15,0)):

    cross_corr = []
    for lag in range(lag_range[0], lag_range[1] + 1):
        if lag < 0:
            # Shift dataframe2 negatively (dataframe1 leads dataframe2)
            shifted_df2 = dataframe2.shift(-lag)
        else:
            # Shift dataframe2 positively (dataframe2 leads dataframe1)
            shifted_df2 = dataframe2.shift(lag)
        
        aligned_df1, aligned_df2 = dataframe1.align(shifted_df2, join='inner', axis=0)
        valid_data = pd.concat([aligned_df1, aligned_df2], axis=1).dropna()

        if not valid_data.empty:
            corr_value = valid_data.corr().iloc[0, 1]         
            cross_corr.append((round(corr_value, 3), lag))  
        else:
            cross_corr.append((None, lag))  

    filtered_corr = [item for item in cross_corr if item[0] is not None]
    sorted_corr = sorted(filtered_corr, key=lambda x: x[0], reverse=True)
    top_3_corr = sorted_corr[:3]

    return top_3_corr

def plot_correlation_data(correlation_data):
    
    lags = [lag for sublist in correlation_data for _, lag in sublist]
    correlations = [correlation for sublist in correlation_data for correlation, _ in sublist]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(lags, correlations, color='blue', marker='o')
    plt.title("E cross-correlation with A vs lag")
    plt.xlabel("Lag")
    plt.ylabel("Correlation")
    plt.grid(True)
    plt.show()


top_3_correlations = []

for i in range(15):
    A_sampled = pd.read_csv(file_paths_A[i])
    B_sampled = pd.read_csv(file_paths_E[i])
    A_sampled = A_sampled.drop(columns=["volume"]).sort_values(by='timestamp')
    B_sampled = B_sampled.drop(columns=["volume"]).sort_values(by='timestamp')
    top_3_correlations.append(compute_cross_correlation(A_sampled['price'], B_sampled['price']))

print(top_3_correlations)

plot_correlation_data(top_3_correlations)