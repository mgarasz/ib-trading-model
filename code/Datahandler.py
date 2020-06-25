import pandas as pd
import talib as tb
import random
import numpy as np
from collections import deque
from sklearn import preprocessing


class DataHandler:
    
    def __init__(self):
        
        self.data = None
        self.threshold = 1.004
        self.future_periods = 1
        
    def get_data(self, url, format_type='csv', return_data=True):
        
        if format_type=='csv':
            
            self.data = pd.read_csv(url)
        
        elif format_type=='json':
            self.data = pd.read_json(url)
           
        else:
            raise("Incorrect format type")
        
        if return_data:
            return self.data
        
    def get_ta(self):
        
            # define pivot variables for easy use
        open_price = self.data['open_price'].values
        close = self.data['close'].values
        high = self.data['high'].values
        low = self.data['low'].values
        volume = self.data['volume'].values
        # define the technical analysis matrix
        retn = np.array([
            tb.MA(close, timeperiod=5),                                         # 1
            tb.MA(close, timeperiod=10),                                        # 2
            tb.MA(close, timeperiod=20),                                        # 3
            tb.MA(close, timeperiod=60),                                        # 4
            tb.MA(close, timeperiod=90),                                        # 5
            tb.MA(close, timeperiod=120),                                       # 6
    
            tb.ADX(high, low, close, timeperiod=20),                            # 7
            tb.ADXR(high, low, close, timeperiod=20),                           # 8
    
            tb.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)[0],    # 9
            tb.RSI(close, timeperiod=14),                                       # 10
    
            tb.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[0],  # 11
            tb.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1],  # 12
            tb.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2],  # 13
    
            tb.AD(high, low, close, volume),                                    # 14
            tb.ATR(high, low, close, timeperiod=14),                            # 15
    
            tb.HT_DCPERIOD(close),                                              # 16
    
            tb.CDL2CROWS(open_price, high, low, close),                               # 17
            tb.CDL3BLACKCROWS(open_price, high, low, close),                          # 18
            tb.CDL3INSIDE(open_price, high, low, close),                              # 19
            tb.CDL3LINESTRIKE(open_price, high, low, close),                          # 20
            tb.CDL3OUTSIDE(open_price, high, low, close),                             # 21
            tb.CDL3STARSINSOUTH(open_price, high, low, close),                        # 22
            tb.CDL3WHITESOLDIERS(open_price, high, low, close),                       # 23
            tb.CDLABANDONEDBABY(open_price, high, low, close, penetration=0),         # 24
            tb.CDLADVANCEBLOCK(open_price, high, low, close),                         # 25
            tb.CDLBELTHOLD(open_price, high, low, close),                             # 26
            tb.CDLBREAKAWAY(open_price, high, low, close),                            # 27
            tb.CDLCLOSINGMARUBOZU(open_price, high, low, close),                      # 28
            tb.CDLCONCEALBABYSWALL(open_price, high, low, close),                     # 29
            tb.CDLCOUNTERATTACK(open_price, high, low, close),                        # 30
            tb.CDLDARKCLOUDCOVER(open_price, high, low, close, penetration=0),        # 31
            tb.CDLDOJI(open_price, high, low, close),                                 # 32
            tb.CDLDOJISTAR(open_price, high, low, close),                             # 33
            tb.CDLDRAGONFLYDOJI(open_price, high, low, close),                        # 34
            tb.CDLENGULFING(open_price, high, low, close),                            # 35
            tb.CDLEVENINGDOJISTAR(open_price, high, low, close, penetration=0),       # 36
            tb.CDLEVENINGSTAR(open_price, high, low, close, penetration=0),           # 37
            tb.CDLGAPSIDESIDEWHITE(open_price, high, low, close),                     # 38
            tb.CDLGRAVESTONEDOJI(open_price, high, low, close),                       # 39
            tb.CDLHAMMER(open_price, high, low, close),                               # 40
            tb.CDLHANGINGMAN(open_price, high, low, close),                           # 41
            tb.CDLHARAMI(open_price, high, low, close),                               # 42
            tb.CDLHARAMICROSS(open_price, high, low, close),                          # 43
            tb.CDLHIGHWAVE(open_price, high, low, close),                             # 44
            tb.CDLHIKKAKE(open_price, high, low, close),                              # 45
            tb.CDLHIKKAKEMOD(open_price, high, low, close),                           # 46
            tb.CDLHOMINGPIGEON(open_price, high, low, close),                         # 47
            tb.CDLIDENTICAL3CROWS(open_price, high, low, close),                      # 48
            tb.CDLINNECK(open_price, high, low, close),                               # 49
            tb.CDLINVERTEDHAMMER(open_price, high, low, close),                       # 50
            tb.CDLKICKING(open_price, high, low, close),                              # 51
            tb.CDLKICKINGBYLENGTH(open_price, high, low, close),                      # 52
            tb.CDLLADDERBOTTOM(open_price, high, low, close),                         # 53
            tb.CDLLONGLEGGEDDOJI(open_price, high, low, close),                       # 54
            tb.CDLLONGLINE(open_price, high, low, close),                             # 55
            tb.CDLMARUBOZU(open_price, high, low, close),                             # 56
            tb.CDLMATCHINGLOW(open_price, high, low, close),                          # 57
            tb.CDLMATHOLD(open_price, high, low, close, penetration=0),               # 58
            tb.CDLMORNINGDOJISTAR(open_price, high, low, close, penetration=0),       # 59
            tb.CDLMORNINGSTAR(open_price, high, low, close, penetration=0),           # 60
            tb.CDLONNECK(open_price, high, low, close),                               # 61
            tb.CDLPIERCING(open_price, high, low, close),                             # 62
            tb.CDLRICKSHAWMAN(open_price, high, low, close),                          # 63
            tb.CDLRISEFALL3METHODS(open_price, high, low, close),                     # 64
            tb.CDLSEPARATINGLINES(open_price, high, low, close),                      # 65
            tb.CDLSHOOTINGSTAR(open_price, high, low, close),                         # 66
            tb.CDLSHORTLINE(open_price, high, low, close),                            # 67
            tb.CDLSPINNINGTOP(open_price, high, low, close),                          # 68
            tb.CDLSTALLEDPATTERN(open_price, high, low, close),                       # 69
            tb.CDLSTICKSANDWICH(open_price, high, low, close),                        # 70
            tb.CDLTAKURI(open_price, high, low, close),                               # 71
            tb.CDLTASUKIGAP(open_price, high, low, close),                            # 72
            tb.CDLTHRUSTING(open_price, high, low, close),                            # 73
            tb.CDLTRISTAR(open_price, high, low, close),                              # 74
            tb.CDLUNIQUE3RIVER(open_price, high, low, close),                         # 75
            tb.CDLUPSIDEGAP2CROWS(open_price, high, low, close),                      # 76
            tb.CDLXSIDEGAP3METHODS(open_price, high, low, close)                      # 77
        ]).T
    
        retdf = pd.DataFrame(retn)
        retdf['date'] = self.data.index.values
        retdf.set_index('date', inplace=True)
        self.data = self.data.join(retdf)
        
        return self.data


    def classify(self, current, future):
        
        if float(future) > float(current*self.threshold):  # if the future price is SUFFICIENTLY higher than the current, that's a buy, or a 1
            return 1
        else:  # otherwise... it's a 0!
            return 0    
    
    def preprocess_df(self, df, normalize=False):
        
        df = df.drop("future", 1)  # don't need this anymore.
        
        ignore = ['temp']
    
        if normalize == True:
            for col in df.columns:  # go through all of the columns
                if col not in ignore:  # normalize all ... except for the target itself!
                    df[col] = df[col].pct_change()  # pct change "normalizes" the different currencies (each crypto coin has vastly diff values, we're really more interested in the other coin's movements)
                    df.dropna(inplace=True)  # remove the nas created by pct_change
                    df[col] = preprocessing.scale(df[col].values)
                    # scale between 0 and 1.
                elif col != 'target':
                    df.dropna(inplace=True)  # remove the nas created by pct_change
                    df[col] = preprocessing.scale(df[col].values) 
                else:
                    pass
            
        df.dropna(inplace=True)  # cleanup again... jic.
        
        sequential_data = []  # this is a list that will CONTAIN the sequences
        prev_days = deque(maxlen=self.SEQ_LEN)  # These will be our actual sequences. They are made with deque, which keeps the maximum length by popping out older values as new ones come in
        
        for i in df.values:  # iterate over the values
            prev_days.append([n for n in i[:-1]])  # store all but the target
            if len(prev_days) == self.SEQ_LEN:  # make sure we have 60 sequences!
                sequential_data.append([np.array(prev_days), i[-1]])  # append those bad boys!
        
        random.shuffle(sequential_data)  # shuffle for good measure.
        
        buys = []  # list that will store our buy sequences and targets
        sells = []  # list that will store our sell sequences and targets
        
        for seq, target in sequential_data:  # iterate over the sequential data
            if target == 0:  # if it's a "not buy"
                sells.append([seq, target])  # append to sells list
            elif target == 1:  # otherwise if the target is a 1...
                buys.append([seq, target])  # it's a buy!
    
        random.shuffle(buys)  # shuffle the buys
        random.shuffle(sells)  # shuffle the sells!
        
        lower = min(len(buys), len(sells))  # what's the shorter length?
        
        buys = buys[:lower]  # make sure both lists are only up to the shortest length.
        sells = sells[:lower]
        
        sequential_data = buys+sells  # add them together
        random.shuffle(sequential_data)  # another shuffle, so the model doesn't get confused with all 1 class then the other.
        
        X = []
        y = []
        
        for seq, target in sequential_data:  # going over our new sequential data
            X.append(seq)  # X is the sequences
            y.append(target)  # y is the targets/labels (buys vs sell/notbuy)
        
        return np.array(X), y


    def label_data(self):
    
        self.data['future'] = self.data["high"].shift(-self.future_periods)
        self.data['target'] = list(map(self.classify, self.data["close"], self.data['future']))
        
    
    
    
    
    