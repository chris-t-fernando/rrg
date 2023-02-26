"""
Calculate both a 10 and 30 week SMA
Take MACD of above
Create RS Ratio using MACD and Julius proprietary factor (1-99)
Calculate 9 week SMA of RS Ratio
Create RS Momentum of above.
Plot RS Ratio vs. RS Momentum
"""

from symbol import SymbolData
import btalib

window = 30
z = SymbolData("^AXIJ", "1d")


btadf = btalib.macd(z.bars, pfast=10, pslow=30).df

# 100+ ((Value-Mean)/Standard Dev) +1
rs = btadf.macd
rs_ratio = rs.rolling(window)
rel_ratio = 100 + ((rs - rs_ratio.mean()) / rs_ratio.std(ddof=1) + 1)
print("a")


"""

#Normalize the Values considering a 14-days Window (Note: 10 weekdays)
for ticker in indices_currencies_data_table.columns: 
    indices_currencies_data_table[ticker] = 100 + ((indices_currencies_data_table[ticker] - indices_currencies_data_table[ticker].rolling(10).mean())/indices_currencies_data_table[ticker].rolling(10).std() + 1)
    
# Rouding and Exclusing NA's
"""
