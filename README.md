# backtest
a simple implement of backtest program
# how to use
first , run data_generate.py to down data from binance <br>
then run backtest program , enter imformation in need , result will output to result.txt <br>
# stradegy
I use double SMA cross stradegy to test , you can change it in source code : class stradegy <br>
in stradegy::run , it will return a tuple :  <br>
* startTime : nth kline buy  <br>
* endTime : nth kline sell <br>
* startPrice : price when buy  <br>
* endPrice : price when sell  <br>
* status : describe about the trade : <br>
    * 0 : long  
    * 1 : short 
    * -1 : Liquidation 
# notice
this program is a simple implement , many detail is not complete enough(ex. fundingRate is ignore . price is only use random function to simulate) , so  don't completly depend on the result
# environment
### ubuntu 20.4 LST
### python 3.8
### c++17
