from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
import pandas as pd
import time

class IBConnect:
    
    def __init__(self):
        
        self.symbol = 'QQQ'
        self.order_id = None 
        self.port = 4002
        self.clientId = 666
        self.account_id = 'YOUR ACCOUNT ID'
        self.total_usd_cash = None
        self.current_position_value = None
    
    def get_current_order_id(self):

        order_id_rec = pd.read_csv('order_id.csv')
        self.order_id = int(order_id_rec.iloc[0][0])
        
    def update_order_id(self):
        
        order_id_rec = pd.read_csv('order_id.csv')
        order_id_rec.iloc[0][0] = int(self.order_id)
        order_id_rec.to_csv('order_id.csv', index=False)
        
    def make_contract(self, symbol, sec_type, exch, prim_exch, curr):
    
        Contract.m_symbol = self.symbol
        Contract.m_secType = sec_type
        Contract.m_exchange = exch
        Contract.m_primaryExch = prim_exch
        Contract.m_currency = curr
        return Contract
    
    
    def make_order(self, action,quantity, price=None):
    
        if price is not None:
            order = Order()
            order.m_orderType = 'LMT'
            order.m_totalQuantity = quantity
            order.m_action = action
            order.m_lmtPrice = price
    
        else:
            order = Order()
            order.m_orderType = 'MKT'
            order.m_totalQuantity = quantity
            order.m_action = action
    
        return order
    
    
    def place_order(self, action='BUY', quantity=500):
        
        self.get_current_order_id()
        
        conn = Connection.create(port=self.port, clientId=self.clientId)
        conn.connect()
        conn.registerAll(self.handleAll)
        
        cont = self.make_contract('QQQ', 'STK', 'SMART', 'SMART', 'USD')
        offer = self.make_order(action, quantity)
        conn.placeOrder(self.order_id, cont, offer)
        
        self.order_id += 1
        self.update_order_id()
        
        conn.disconnect()
        
        return
    
    def request_account_summary(self):
        
        # test this 
        conn = Connection.create(port=self.port, clientId=self.clientId)
        conn.connect()
        time.sleep(1)
        
        conn.register(self.handleAll,
                 message.updateAccountValue,
                 message.updateAccountTime,
                 message.updatePortfolio)
        
        conn.reqAccountUpdates(True, self.account_id)
        conn.disconnect()

    def request_current_positions(self):
        
        # test this 
        conn = Connection.create(port=self.port, clientId=self.clientId)
        conn.connect()
        time.sleep(5)

        conn.register(self.handlePositions,
                 message.accountSummary
                 )
        
        conn.reqAccountSummary(9003, "All", "GrossPositionValue")
        time.sleep(5)
        conn.disconnect()
        
    def request_cash_balance(self):
        
        conn = Connection.create(port=self.port, clientId=self.clientId)
        conn.connect()
        time.sleep(5)
        #conn.registerAll(self.handleAll)
        conn.register(self.handleCashBalance,
                message.accountSummary)
        
        conn.reqAccountSummary(9003, "All", "$LEDGER:USD")
        time.sleep(5)
        conn.disconnect()
        
        
    def handleCashBalance(self, msg):
        
        if msg.tag == 'TotalCashBalance':    
            self.total_usd_cash = float(msg.value)
            print(msg)
    
    def handlePositions(self, msg):
        
        if msg.tag == 'GrossPositionValue':    
            self.current_position_value = float(msg.value)
            print(msg)
        
    
    def handleAll(self, msg):
        print(msg)
        







