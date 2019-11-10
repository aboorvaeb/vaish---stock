import numpy as np  
import pandas as pd  
from pandas_datareader import data as wb  
import matplotlib.pyplot as plt  
from scipy.stats import norm
import matplotlib.mlab as mlab

class monte_carlo:
    
    def __init__(self, ticker):
        data = pd.DataFrame()
        data[ticker] = wb.DataReader(ticker, data_source='yahoo', start='2018-1-1')['Adj Close']
        log_returns = np.log(1 + data.pct_change())
        
        self.ticker = ticker
        self.data = data
        self.log_returns = log_returns
    
    def plot_historical_data(self):
        data = self.data
        ticker = self.ticker
        log_returns = self.log_returns
    
        data.plot(figsize=(10, 6),color='red');
        plt.ylabel('Price')
        plt.title('Historical Price of '+str(ticker)+' Stock',fontsize=18, fontweight='bold')
        plt.savefig('1.png')

        log_returns.plot(figsize = (10, 6))
        plt.ylabel("Log Returns")
        plt.title('Historical Log Returns',fontsize=18, fontweight='bold')
        plt.savefig('2.png')
    
        
    def brownian_motion(self,sim_days,sim_num,show_hist = True):
        data = self.data
        log_returns = self.log_returns
        ticker = self.ticker
        
        u = log_returns.mean()
        var = log_returns.var()
        
        drift = u - (0.5 * var)        
        daily_volatility = log_returns.std()
    
        shock = drift.values + daily_volatility.values*norm.ppf(np.random.rand(sim_days, sim_num))
    
        daily_returns = np.exp(shock)
        
        last_price = data.iloc[-1]
        
        price_list = np.zeros_like(daily_returns)        
        price_list[0] = last_price
        
        for t in range(1, sim_days):
            price_list[t] = price_list[t - 1] * daily_returns[t]
            
        plt.figure(figsize=(10,6))
        plt.plot(price_list)
        plt.title(str(sim_days)+' Days Monte Carlo Simulation for '+ str(ticker))
        plt.xlabel('Days')
        plt.ylabel('Price ($)')
        #plt.show()
        plt.savefig('3.png')

        price_array = price_list[-1]
        start = price_array.mean() - norm.ppf(0.56)*np.std(price_array)
        end = price_array.mean() + norm.ppf(0.56)*np.std(price_array)
    
        retval_str = "Probability price is between $"+ str(round(start,2)) +" and $"+ str(round(end,2)) +": " + "{0:.2f}%".format((float(len(price_array[(price_array > start) & (price_array < end)])) / float(len(price_array)) * 100))
        self.price_array = price_array
        most_prob_price = price_array[(price_array > start) & (price_array < end)].mean()
        retval_str1 = "Most probable price is $"+ str(round(most_prob_price,2))

        if show_hist:
            self.histogram(price_list[-1],last_price,most_prob_price)

        return retval_str,retval_str1
            
            
    def histogram(self,ser,last_price,most_prob_price):
    
        x = ser
        mu = ser.mean()
        sigma = ser.std()
        
        num_bins = 20
        # the histogram of the data
        plt.figure(figsize=(10,6))
        n, bins, patches = plt.hist(x, num_bins, rwidth=0.9, density=1, facecolor='green', alpha=0.6)
             
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Price')
        plt.ylabel('Probability')
        plt.title(r'Histogram of Simulated Stock Prices', fontsize=18, fontweight='bold')
        plt.axvline(x=last_price.values, color='black', linestyle='--', label = 'Current Stock Price: '+str(round(last_price.values[0],2)))
        plt.axvline(x=most_prob_price, color='blue', linestyle='--', label = 'Predicted Price: '+str(round(most_prob_price,2)))
        plt.legend(loc="upper right")
        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        
        #plt.show()
        plt.savefig('4.png')    
        