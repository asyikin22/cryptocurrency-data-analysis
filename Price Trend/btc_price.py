from pycoingecko import CoinGeckoAPI
import pandas as pd
import matplotlib.pyplot as plt

#initialize the coingecko API client

cg = CoinGeckoAPI()

#fetch historical price data for Bitcoin (BTC) for the last 30 days
data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='myr', days=365)

#convert price data into df
prices = pd.DataFrame(data['prices'], columns=['Timestamp', 'Price'])

#convert time stamp from ms to date time object
prices['Timestamp'] = pd.to_datetime(prices['Timestamp'], unit='ms')

# print(prices.head())

#plot price trend
plt.figure(figsize=(10,6))
plt.plot(prices['Timestamp'], prices['Price'], label='Bitcoin Price')
plt.xlabel('Date')
plt.ylabel('Price (MYR)')
plt.title('Bitcoin Price Trend Over the Last 365 Days')
plt.legend()
plt.grid(True)
plt.show()

#Claculate basic statistics
average_price = prices['Price'].mean()
max_price = prices['Price'].max()
min_price = prices['Price'].min()

print(f'Average price: RM{average_price:.2f}')
print(f'Highest Price: RN{max_price:.2f}')
print(f"Lowest Price: RM{min_price:.2f}")