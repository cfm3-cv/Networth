from financeData import cashFlowAdjustments
from financeData import EquityBucket
# Parametric Inputs
stock_app_nom = 0.10
cap_appreciation_nom = 0.05
rent_inflation_nom = 0.06
inflation = 0.03
T0_nw = 900000
Period = 30 # Number of years we want to run the calculation on
T0_Rent = 5000
T0_HomeVal = 1500000

# Derived Inputs
cap_appreciation_real = cap_appreciation_nom - inflation
stock_app_real = stock_app_nom - inflation
rent_inflation_real = rent_inflation_nom - inflation


cashFlow = cashFlowAdjustments(Period)
cashFlow.addCashAdj(5000, 2)
cashFlow.addCashAdj(8888, 5)




''' Approach
Create lists of values, which represent equity buckets and cash in/outflows
These lists will represent a time-based sequence of present-values
The NetWorth class will have a corresponding object for each of these classes
Parameters will be defined at the beginning, and used to calculate each equity bucket and in/outflow

Equity Buckets:
- Stock equity
- Home value

Cash Outflows
- Maintenance
- Property taxes paid
- Homeowners insurance
- Closing costs
- Monthly mortgage payment
- Monthly Rent payment
- Down Payment


Cash Inflows
- Morgage interest tax deduction
- Monthly Salary
- SALT deduction
- Standard deduction

'''

'''
class Scenario:
# Placeholder for a class which runs a scenario
# This class instance will have a list of EquityBuckets, and list of CashFlow
'''


homeEquity = EquityBucket(1000000, cap_appreciation_real)
home_vals = homeEquity.calculate_vals()

investments = EquityBucket(5000, stock_app_real)
investments.addCashFlows(cashFlow.cashAdjustmentsList)

current_year = 0
while current_year <= Period:
    investments.calculate_vals(current_year)
    current_year = current_year + 1

investments.reportFinancials("Investments")
homeEquity.reportFinancials("Home Equity")
