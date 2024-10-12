from pycoingecko import CoinGeckoAPI
import pandas as pd
import matplotlib.pyplot as plt

#initialize coingecko API client

cg = CoinGeckoAPI()

#list of coins to compare
coins = ['bitcoin', 'ethereum', 'tether', 'binancecoin']

#fetch historical price data for the last 180 days
price_data = {}
for coin in coins:
    try:
        data = cg.get_coin_market_chart_by_id(id=coin, vs_currency='myr', days=180)
        prices = pd.DataFrame(data['prices'], columns=['Timestamp', 'Price'])
        prices['Timestamp'] = pd.to_datetime(prices['Timestamp'], unit='ms')
        price_data[coin] = prices
    except Exception as e:
        print(f"failed to fetch data for {coin}: {e}")

#print the head of each df in the dictionary
for coin, prices in price_data.items():
    print(f"{coin} price data:\n{prices.head()}\n")
    

#Calculate basic stats for each coin
for coin, prices in price_data.items():
    if prices.empty:
        print(f'No data returned for {coin}')
        continue
    
    #calculate stats
    mean_price = prices['Price'].mean()
    median_price = prices['Price'].median()
    max_price = prices['Price'].max()
    min_price = prices['Price'].min()
    std_dev_price = prices['Price'].std()
    
    #print
    print(f"{coin} price statistics:")
    print(f"  Mean Price: RM{mean_price:.2f}")
    print(f"  Median Price: RM{median_price:.2f}")
    print(f"  Max Price: RM{max_price:.2f}")
    print(f"  Min Price: RM{min_price:.2f}")
    print(f"  Std Dev: RM{std_dev_price:.2f}")
    print("\n" + "x"*40 +"\n")
    
#Visualize price data
plt.figure(figsize=(14,10))

#create subplot for each coin
for i, coin in enumerate(coins, 1):
    if coin in price_data:
        prices = price_data[coin]
        plt.subplot(2, 2, i)         #2x2 grid subplot
        plt.plot(prices['Timestamp'], prices['Price'], label=coin)
        plt.title(f"{coin.capitalize()} Price Over Last 180 Days")
        plt.xlabel('Data')
        plt.ylabel('Price (RM)')
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()

#adjust layout
plt.tight_layout()
plt.show()

# #visualzie price data
# plt.figure(figsize=(14,7))

# for coin in coins:
#     if coin in price_data:
#         prices = price_data[coin]
#         plt.plot(prices['Timestamp'], prices['Price'], label=coin)
        

# #customize chart
# plt.title("Cryptocurrency Prices over Last 80 Days")
# plt.xlabel("Date")
# plt.ylabel("Price (RM)")
# plt.grid()
# plt.legend()
# plt.tight_layout()
# plt.show()