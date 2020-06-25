import numpy as np
import pandas as pd
import pickle
import ta

import schedule
import time
from datetime import datetime, date

from ib.opt import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order

from IBManager import IBConnect
from LongModel import LongModel
from Datahandler import Datahandler

# ... instantiate all relevant classes
IB = IBConnect()
agent = LongModel()
agent.import_model('XGBoost_long20190431.sav')
data = Datahandler()


# ... define jobs
def exit_positions():
    
    IB = IBConnect()

    print('Position exit function:', datetime.now())
    IB.request_current_positions()
    
    if IB.current_position_value != 0.0:
        IB.place_order(action='SELL')
        print('Sell order placed')
    else:
        print('No positions held')
        # show current cash balance as well afterwards


def record_keeper():
    
    IB = IBConnect()
    
    print('Record function:', datetime.now())
    today_id = date.today().year * 10000 + date.today().month*100 + date.today().day
    IB.request_cash_balance()
    cash = IB.total_usd_cash

    past_records = pd.read_csv(r'C:\Users\MikeG\Python Stuff\crypto_data\XGB Trading Model\records.csv')
    if today_id not in past_records.date.unique():
        past_records = pd.concat([past_records, pd.DataFrame(columns=['date','cash'], 
                                                             data={'date': [today_id], 
                                                                   'cash': [cash]})])
    past_records.to_csv('records.csv', index=False)


def enter_positions():
    
    IB = IBConnect()
    
    print('Position enter function:', datetime.now())
    data.get_data()
    data.calculate_indicators()
    today = data.return_latest_data()
    decision = agent.classify(today)
    
    if decision == 1:
        IB.place_order(action='BUY', quantity=500)
        print('Entry made')
    else:
        print('Entry criteria for today not met - no position taken.')
    


def running_confirmation():
    print('Algo still active: ', datetime.now())

print('Algo running:', datetime.now())
# ... schedule jobs
schedule.every(10).minutes.do(running_confirmation)
schedule.every().day.at("14:31").do(exit_positions) #9:31am in NYC
schedule.every().day.at("15:00").do(record_keeper) #9:31am in NYC
schedule.every().day.at("20:45").do(enter_positions) #3:31pm in NYC


while 1:
    schedule.run_pending()
    time.sleep(1)