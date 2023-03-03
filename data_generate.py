from src.binanceApi import binanceApi
import csv
import time
'''
setting:
    symbol : btcusdt
    interval : 1m
    startTime : 2020-01-01 0:0:0
    endTime : 2022-12-31 23:59:59
    output : data.csv
'''
a = binanceApi()
startTime = a.dateStr2ts('2020-01-01 0:0:0')
endTime = a.dateStr2ts('2022-12-31 23:59:59')
intervalPerms = 60000 # convert interval to ms
with open('data.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([(endTime+1000-startTime)/intervalPerms])
    writer.writerow([startTime])
    while(endTime>startTime):
        if(startTime+86399999<endTime):
            writer.writerows(a.Kline_Data(symbol='btcusdt',interval='1m',limit=1500,startTime=startTime,endTime=startTime+86399999))
        else :
            writer.writerows(a.Kline_Data(symbol='btcusdt',interval='1m',limit=1500,startTime=startTime,endTime=endTime))
        startTime += 86400000
        time.sleep(0.1) #limit : 2400 / min