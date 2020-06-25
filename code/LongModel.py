import pandas as pd
import pickle

class LongModel:
    
    
    def __init__(self):
        
        self.model = None
        self.data = None

    def import_model(self, filename):
        
        loaded_model = pickle.load(open(filename, 'rb'))
        self.model = loaded_model
        return
        
    def intake_data(self, data):
        
        self.data = data
        pass

    def classify(self, data):
        
        #self.intake_data(data)
        data = pd.to_numeric(data)
        X = pd.DataFrame(data[['open_delta', 'RVI', 'V-SMA', 'SMA', 'VPT']])
        X = X.T
        decision = self.model.predict(X)
        
        return decision[-1]
        

        
        
    
    
    
    
    
    