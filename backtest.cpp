#include<iostream>
#include<string>
#include<sstream>
#include<fstream>
#include<vector>
#include<iomanip>
#include<random>
#include<climits>

using namespace std;
using tp = tuple<int,int,double,double,int>;

//create stradegy there
class stradegy
{
private:
    int lever;
    double stopLoss;
    double takeProfit;
    vector<double> longPoint; //long
    vector<double> shortPoint; //short
public:
    stradegy(int lever, double stopLoss, double takeProfit)
    {
        this->lever = lever;
        this->stopLoss = stopLoss; //stop loss 
        this->takeProfit = takeProfit; //take profit 
    }

    ~stradegy()
    {
        longPoint.clear();
        shortPoint.clear();
    }

    double RandomNumber(double Min, double Max)
    {
        return ((double(rand()) / double(RAND_MAX)) * (Max - Min)) + Min;
    }

    vector<double> SMA(vector<double> &close, int period)
    {
        int n = close.size();
        double sum = 0;
        vector<double> _SMA(n,0);
        if(n < period)
            return _SMA;
        for(int i = 0; i < period - 1; ++i)
        {
            sum += close[i];
        }
        for(int i = period - 1; i < n; ++i)
        {
            sum += close[i];
            _SMA[i] = (sum / period);
            sum -= close[i- period - 1];
        }
        return _SMA;
    }
    /*
        test Stradegy,use two sma whith different period
        when they cross , trade
    */
    void testStradegy(vector<double>& close)
    {
        int n = close.size();
        auto SSMA = SMA(close, 60);
        auto LSMA = SMA(close, 120);
        
        int condition = 0;
        for(int i = 0;i < n; ++i)
        {
            if(LSMA[i] == 0) continue;
            if (condition == 0)
            {
                if(LSMA[i] > SSMA[i])
                {
                    condition = 1;
                }
                else if(LSMA[i] < SSMA[i])
                {
                    condition = -1;
                }
            }
            else if(condition == 1)
            {
                //long
                if(LSMA[i] < SSMA[i])
                {
                    longPoint[i] = 1;
                    condition = -1;
                }
            }
            else
            {
                //short
                if(LSMA[i] > SSMA[i])
                {
                    shortPoint[i] = 1;
                    condition = 1;
                }
            }
        }
        SSMA.clear();
        LSMA.clear();
    }

    vector<tp> run(vector<double>& high, vector<double>& low, vector<double>& close)
    {
        vector<tp> res;
        int startTime, endTime, status, n = close.size();
        double startPrice, endPrice;

        longPoint.resize(n,-1);
        shortPoint.resize(n,-1);
        srand(time(nullptr));

        //run stradegy
        testStradegy(close);

        for(int i = 0; i < close.size(); ++i)
        {
            double stopLossPoint; // stop loss point
            double takeProfitPoint; // take profit point
            double liquidationPoint; // Liquidation point
            //long
            if(longPoint[i] == 1)
            {
                startTime = i;
                startPrice = close[i];
                stopLossPoint = stopLoss == -0.01 ? 0 : startPrice * (1 - stopLoss / double(lever));
                takeProfitPoint = takeProfit == -0.01 ? INT_MAX : startPrice * (1 + takeProfit / double(lever));
                liquidationPoint = startPrice * (1 - 1.0 / double(lever));
                status = 0;

                ++i;
                for(; i < n; ++i)
                {
                    if(high[i] >= takeProfitPoint)
                    {
                        //take profit
                        endTime = i;
                        endPrice = RandomNumber(takeProfitPoint, high[i]);
                        break;
                    }
                    else if(low[i] <= liquidationPoint)
                    {
                        //may Liquidation
                        endTime = i;
                        endPrice = RandomNumber(low[i], stopLossPoint);
                        
                        if(endPrice <= liquidationPoint)
                        {
                            //Liquidation
                            status = -1;
                            endPrice = liquidationPoint;
                        }    
                        break;
                    }
                    else if(low[i] <= stopLossPoint)
                    {
                        //stop loss
                        endTime = i;
                        endPrice = RandomNumber(low[i], stopLossPoint);
                        break;
                    }
                }
                if(startTime > endTime) 
                    continue;
                res.push_back(make_tuple(startTime,endTime,startPrice,endPrice,status));
                continue;
            }

            //short
            if( shortPoint[i] == 1)
            {
                startTime = i;
                startPrice = close[i];
                stopLossPoint = stopLoss == -0.01 ? INT_MAX : startPrice * (1 + stopLoss / double(lever) * 1.0);
                takeProfitPoint = takeProfit == -0.01 ? 0 : startPrice * (1 - takeProfit / double(lever) * 1.0);
                liquidationPoint = startPrice * (1 + 1.0 / double(lever));
                status = 1;

                ++i;
                for(; i< n; ++i)
                {
                    if(low[i] <= takeProfitPoint)
                    {
                        //take profit
                        endTime = i;
                        endPrice = RandomNumber(low[i], takeProfitPoint);
                        
                        break;
                    }
                    else if(high[i] >= liquidationPoint)
                    {
                        //may Liquidation
                        endTime = i;
                        endPrice = RandomNumber(stopLossPoint, high[i]);
                        
                        if(endPrice >= liquidationPoint)
                        {
                            //Liquidation
                            status = -1;
                            endPrice = liquidationPoint;
                        }
                        break;
                    }
                    else if(high[i] >= stopLossPoint)
                    {
                        //stop loss
                        endTime = i;
                        endPrice = RandomNumber(stopLossPoint, high[i]);
                        break;
                    }
                }
                if(startTime > endTime) 
                    continue;
                res.push_back(make_tuple(startTime,endTime,startPrice,endPrice,status));
            }
        }
        
        return res;
    }
};

class readData
{
private:
    string filename;
public:
    vector<double> open; //price when startTime
    vector<double> high; //highest price
    vector<double> low; //lowest price
    vector<double> close; //price when endTime 
    time_t timestamp; //start time of data

    readData(string filename)
    {
        this->filename = filename;
    }

    readData(){}

    ~readData()
    {
        open.clear();
        high.clear();
        low.clear();
        close.clear();
        filename.clear();
    }

    //read data
    void read()
    {
        ifstream file;
        string row;
        file.open(filename);

        long long n = 0;
        int index = 0;
        getline(file,row);
        n = stoll(row);
        getline(file,row);
        timestamp = (stoll(row) / 1000);
        
        open.resize(n);
        high.resize(n);
        low.resize(n);
        close.resize(n);

        while(getline(file,row))
        {
            stringstream ss(row);
            string data;
            getline(ss,data,',');
            int i = 0;
            while (i < 4 && getline(ss,data,','))
            {
                switch (i)
                {
                    case 0:
                        open[index] = stod(data);
                        break;
                        
                    case 1:
                        high[index] = stod(data);
                        break;
                        
                    case 2:
                        low[index] = stod(data);
                        break;

                    case 3:
                        close[index] = stod(data);
                        break;
                        
                    default:
                        break;
                }
                ++i;
            }
                ++index;
        }
        file.close();
        row.clear();
    }
};

class backtest
{
private:
    double profit; //total profit
    double feeRate; //fee rate
    int lever; //lever
    int interval; //kline interval (m)
    int tradeCount; //times of trade
    int win; // times of positive profit

    ofstream result;//log file
    readData data;

    time_t timestamp;//initial timestamp in data
public:
    backtest(string filename, int lever, int interval, double feeRate)
    {
        profit = 0;
        this->feeRate = feeRate;
        this->lever = lever;
        this->interval = interval;
        win = 0;
        tradeCount = 0;
        
        //load data
        data = readData(filename);
        data.read();
        timestamp = data.timestamp;

        //initial log file
        result.open("result.txt");
        result<<left<<setw(10)<<"times";
        result<<left<<setw(30)<<"startTime";
        result<<left<<setw(15)<<"price";
        result<<left<<setw(30)<<"endTime";
        result<<left<<setw(15)<<"price";
        result<<left<<setw(20)<<"profit(%)";
        result<<left<<setw(10)<<"status"<<endl;
    }
    ~backtest()
    {
        result.close();
    }
    //conver timestamp to date
    string convert2Date(int time)
    {   
        auto newTimestamp = timestamp + time * 60 * interval;
        string date = ctime(&newTimestamp);
        date.pop_back();
        return date;
    }

    //update changes in log file
    void endlog()
    {
        result<<endl<<endl;
        result<<"----------------total----------------"<<endl;
        result<<"   profit : "<<profit * 100<<"%"<<endl;
        result<<"   trade "<<tradeCount<<" times"<<endl;
        result<<"   win rate : "<<double(win) / double(tradeCount) * 100<<"%"<<endl;
    }
    void log(int startTime, int endTime, double startPrice, double endPrice, int status)
    {   
        double profitThisTime;
        string describe;
        if(status == -1)
        {
            profitThisTime = -1;
            describe = "Liquidation";
        }    
        else
        {
            if(status == 1)
            {
                profitThisTime = lever * ((startPrice - endPrice) / startPrice - feeRate * (1 + endPrice / startPrice));
                describe = "Short";
            }
            else
            {
                profitThisTime = lever * ((endPrice - startPrice) / startPrice - feeRate * (1 + endPrice / startPrice));
                describe = "Long";
            }
        }
        if(profitThisTime > 0) ++win;
        profit += profitThisTime;
        result<<left<<setw(10)<<++tradeCount;
        result<<left<<setw(30)<<convert2Date(startTime);
        result<<left<<setw(15)<<startPrice;
        result<<left<<setw(30)<<convert2Date(endTime);
        result<<left<<setw(15)<<endPrice;
        result<<left<<setw(20)<<profitThisTime*100;
        result<<left<<setw(10)<<describe<<endl;
    }

    //run stradegy and summary
    void run(double stopLoss, double takeProfit)
    {
        stradegy st(lever, stopLoss, takeProfit);
        auto results = st.run(data.high, data.low, data.close);
        for(auto &res : results)
        {
            //update changes
            log(get<0>(res), get<1>(res), get<2>(res), get<3>(res), get<4>(res));
        }
        endlog();
    }
};

int main(){
    string filename;
    int lever,interval;
    double stopLoss, takeProfit, feeRate;
    cout<<"filename : ";
    cin>>filename;
    cout<<"lever : ";
    cin>>lever;
    cout<<"kline interval(m) : ";
    cin>>interval;
    cout<<"trade fee rate(%) : ";
    cin>>feeRate;
    cout<<"stopLoss(%) set -1 to ignore : ";
    cin>>stopLoss;
    cout<<"takeProfit(%) set -1 to ignore : ";
    cin>>takeProfit;
    backtest test(filename, lever, interval, feeRate/100);
    test.run(stopLoss/100, takeProfit/100);
    cout<<"done"<<endl;
    return 0;
}   