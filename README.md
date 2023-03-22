# Bot that determines the self-movement of Ethereum price in real-time.
## 1. Choosing a method to determine the self-movement of ETHUSDT price
To determine the self-movement of ETHUSDT price and exclude the influence of BTCUSDT price, the method of linear regression was chosen.

### Advantages of the linear regression method:
* Prediction accuracy: Allows for sufficiently accurate predictions with correctly selected input data.
* Simplicity and convenience: Linear regression is a relatively simple and easily interpretable method that can be used for quickly assessing the relative impact of various factors on the movement of BTCUSDT futures price.
* Considering a combination of factors, this method appears to be optimal for solving the given task.

### Selection of input parameters:
As input parameters to the linear regression algorithm, two arrays containing historical data on BTCUSDT and ETHUSDT prices were passed.
However, to obtain correct results, it should be taken into account that the data passed to the algorithm should be as up-to-date as possible.

## 2. Creating a program to track the price of ETHUSDT
The program tracks the price of ETHUSDT in real-time and determines its self-movement.
To maintain calculation accuracy, it constantly updates historical data on BTCUSDT and ETHUSDT prices.
To improve performance, all tasks are performed asynchronously using libraries such as asyncio and aiohttp.

### The program description is as follows:
* Immediately after starting, the program loads historical data on BTCUSDT and ETHUSDT to train the regression model.
All currency price data is obtained by calling the Binance API. The aiohttp library is used for access.
* Next, the data is passed to the regression model. The scikit-learn library's LinearRegression() class is used as the model.
* Next, using the Binance streaming service, the program receives data on current currency prices, makes a price forecast for ETHUSDT, and excludes the influence of BTCUSDT price.
* If a change in the ETHUSDT price of 1% or more is detected, the program remembers the last value of the ETHUSDT price.
* Outputs information on the last recorded price change once every 60 minutes.
* The cycle then repeats. The program also constantly updates historical data at a set interval and re-trains the model on current data. All tasks are performed asynchronously.

### How to install
To install the program, you need to download all packages from requirements.txt.
1. Go to the root directory of the project.
2. Create and activate a virtual environment.
3. Run the following command:
pip install -r .\requirements.txt

### How to use
To run the program, use the script eth_checker.py located in the root directory.\
The program has several configurable parameters, which can be changed in the config.txt file.

Parameter reference:\
Used to set the start and end date for downloading historical currency price data.
In the format of yyyy-m-d.\
FROM_DATE, TO_DATE

Sets the period for updating historical data (in minutes).\
UPDATE_PERIOD

The parameter sets the frequency of data sampling for historical data.
(For example, daily summaries or hourly, minute data, etc.). An example of input format: 1m, 3h, 2d, 1M.\
SAMPLE_TIME

This parameter sets whether to get detailed information about each step of the program cycle,
as well as about currency prices at each step and the proportion of the ETHUSDT's own price change. (Boolean value).\
PRINT_DETAILED_INFO

