class cashFlowAdjustments:
    # Class which will contain a list of cash flow adjustments to be made to our investments
    # Each discrete adjustment is a tuple, and can be either recurring (year is none)
    # Or one time, in which case the year for the adjustment must be specified
    # These adjustments are stored in the cashAdjustments List, and will be applied
    # sequentially to our investmnets, as the years values are calculated
    
    def __init__(self, period):
        self.period = period
        self.oneTimeCashAdjustmentsList = []
        self.recurringCashAdjustmentsList = []

    
    def addCashAdj(self, cash_val, year = None, recurring = None, app = None):
        adjustment = (cash_val, year)
        self.oneTimeCashAdjustmentsList.append(adjustment)
        return
    
    def getCashAdjList(self):
        return self.cashAdjustmentsList
  

class EquityBucket:
    # Initialize with instance attributes specific to this object

    def __init__(self, T0_val, app_rate):
        self.values = []
        self.T0_val = T0_val
        self.app_rate = app_rate
        self.cashFlowList = None
        self.values.append(T0_val)

    def reportFinancials(self, label):
        print("\n====== " + label + " ======")
        for i in range(len(self.values)):
            print("year " + str(i) + ": " + "${0:6,.0f}".format(self.values[i]))

    def addCashFlows(self, cashFlowList):
        self.cashFlowList = cashFlowList
        
    def calculate_vals(self, year = 0):
        if year == 0:
            return
        else:
            self.values.append(self.values[year-1] * (1+self.app_rate))
            for i in self.cashFlowList:
                if i[1] == year:
                    self.values[year] = self.values[year -1] + i[0]
