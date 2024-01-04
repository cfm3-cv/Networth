import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator,
                               FormatStrFormatter,
                               AutoMinorLocator)
import numpy as np
from mortgage import mortgage


class EquityBucket:
    # values are the time-series list of valuations
    
    def __init__(self, T0_val = 0, app_rate = 0, Period = 30, name = None):
        self.valuations = []
        self.T0_val = T0_val
        self.app_rate = app_rate
        self.valuations.append(T0_val)
        self.Period = Period
        self.cashFlowAdjs = []
        self.name = name
        self.mortgage = None
    
    def generateMortgage(self, interest_rate, T0_loan_amt, app_rate = None):
        self.mortgage = mortgage(interest_rate, T0_loan_amt, self.app_rate)
        self.mortgage.generate_mortgage_schedule()
        #print(self.mortgage.yearly_interest_list)
        #print(self.mortgage.annual_liabilities_list)
        
    def setAppRate(self, apprate):
        self.app_rate = apprate
        
    def adjustCash(self, year, value):
        self.cashFlowAdjs.append((year, value))
        
    def addYearlyInvestments(self, value, years = (0,0)):
        # Add a certain amount of cash investments (net salary after spending) each year
        i = years[0]
        while i < years[1]:
            self.adjustCash(i, value)
            #print(str(i) + " " + str(value))
            i = i+1
    
    def addInvestmentList(self, annual_investments, start_year = 0):
        # Add a list of annual investments to this equity
        i = 0
        while i < len(annual_investments):
            self.adjustCash(i, annual_investments[i])
            i = i + 1

    def printValuations(self):
        for i in range(len(self.valuations)):
            print("year " + str(i) + ": " + "${0:6,.0f}".format(self.valuations[i]))
    
    def updateEquityValues(self):
        # Big For statement to do the annual calucaltions
        for year in range(self.Period):
            # If we have an entry in the cashFlowAdjustments for this year, then make the adjustment
            for entry in self.cashFlowAdjs:
                if entry[0] == year:
                    self.valuations[year] = self.valuations[year] + entry[1]
        
            # Next, Update the equity value for the current year, given the app rate
            self.valuations.append(self.valuations[year] * (1 + self.app_rate))
            
            # Next, if we have a mortgage associated here, we need to remove the liabilities
            if self.mortgage is not None:
                self.valuations[year] = self.valuations[year] - self.mortgage.annual_liabilities_list[year]
                #print(self.valuations[year])
            # Next, make cash adjustments (if needed)

class Scenario:
    def __init__(self, Period = 30):
        self.Period = Period
        self.equities = []
        self.NW = [0] * Period
    
    def printEquities(self):
        for i in self.equities:
            print(i.name)
    
    def addEquity(self, Equity):
        self.equities.append(Equity)
    
    def calculateNW(self):
        self.NW = [0] * (self.Period + 1)
        for i in self.equities:
            self.NW = [sum(j) for j in zip(i.valuations, self.NW)]

        
    def printValuations(self):
        for i in range(len(self.NW)):
            print("year " + str(i) + ": " + "${0:6,.0f}".format(self.NW[i]))
            
    def plotScenario(self):
        fig, ax = plt.subplots()
        ax.set_ylabel('Value')
        ax.set_xlabel('Years')
        fmt = '${x:,.0f}'
        tick = matplotlib.ticker.StrMethodFormatter(fmt)
        ax.yaxis.set_major_formatter(tick)
        self.calculateNW()
        for i in self.equities:
            plt.plot(range(len(i.valuations)), i.valuations, label=i.name)
        plt.plot(range(len(self.NW)), self.NW, label = "Net Worth")
        plt.legend()
        plt.grid()
        plt.show()
        return

'''
def plotNW(NW1, NW2 = None, label1 = None, label2 = None):
    fig, ax = plt.subplots()
    ax.set_ylabel('Value')
    ax.set_xlabel('Years')
    fmt = '${x:,.0f}'
    tick = matplotlib.ticker.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)
    plt.plot(range(len(NW1)), NW1, label = label1)
    if NW2 is not None:
        plt.plot(range(len(NW2)), NW2, label = label2)
    plt.legend()
    plt.show()
'''
    
def calculateSalary(T0_salary, salary_app, Period):
# Returns:
# List of annual salary
# List of income Taxes due at the end of each year
# List of net income, to be added as cashflows for marginal investments

    salary_list = []
    tax_list = []
    salary_list.append(T0_salary)
    tax_list.append(calculate_taxes(T0_salary))
    
    for i in range(Period + 1):
        yearly_salary = salary_list[i] * (1 + salary_app)
        #print("Salary for year " + str(i + 1) + ": " + str(yearly_salary))
        salary_list.append(yearly_salary)
        tax_due = calculate_taxes(yearly_salary)
        tax_list.append(tax_due)
    

    return salary_list, tax_list
    
def calculate_net_cash(salary_list, taxes_due, T0_spending, spending_app, Period, time_range = None):
    # Given yearly salaries and taxes, calculate leftover investment cash given spending
    # The date range is specified (in years) for when this calculation should take place
    # The return value is an array of length Period with zeroes for anything not in the date range
    
    if time_range is None: # If the year range isn't specified, set it to the entire period
        time_range = (1, 30)
    
    spending = []
    spending.append(T0_spending) # First year spending
    net_cash = []
    
    current_year_counter = 0
    year_in_range = 0
    for i in range(Period):
        if time_range[0] < current_year_counter <= time_range[1]:
            # If the current year is within the range, do the following
            annual_spend = spending[year_in_range - 1] * (1 + spending_app)
            spending.append(annual_spend)
            net_cash.append(salary_list[i] - taxes_due[i] - spending[year_in_range - 1])
            year_in_range = year_in_range + 1
        else:
            net_cash.append(0)
        current_year_counter = current_year_counter + 1
        print("Net New Contributions for year " + str(i) + " :" + str(net_cash[-1]))
    
    return net_cash

    
    '''
    for i in range(len(salary_list)):
        annual_spend = spending[i] * (1 + spending_app)
        spending.append(annual_spend)
        net_cash.append(salary_list[i] - taxes_due[i] - spending[i])
        #print("Net New Contributions for year " + str(i) + " :" + str(net_cash[-1]))
    return net_cash
'''
def calculate_taxes(income, standard_deduction = True):
    # Given a list of incomes, return the income taxes due
    # Note: not yet done: FICA taxes, and 401k deductions...but assume these cancel out
    
    if standard_deduction == True:
        fed_income = income - 13850
        state_income = income - 5363
    
    if fed_income < 11000:
        fed_tax_due = fed_income * 0.1
    elif fed_income <= 44725:
        fed_tax_due = (fed_income - 11000) * .12 + 1100
    elif fed_income < 95375:
        fed_tax_due = (fed_income - 44725) * .22 + 5147
    elif fed_income < 182100:
        fed_tax_due = (fed_income - 95375) * 0.24 + 16290
    elif fed_income < 231250:
        fed_tax_due = (fed_income - 182100) * 0.32 + 37104
    else:
        fed_tax_due = (fed_income - 231250) * 0.35 + 52832
        
    if state_income < 10412:
        state_tax_due = state_income * 0.01
    elif state_income <= 24684:
        state_tax_due = (state_income - 10412) * 0.02 + 104.12
    elif state_income < 38959:
        state_tax_due = (state_income - 24684) * 0.04 + 389.56
    elif state_income < 54081:
        state_tax_due = (state_income - 38959) * 0.06 + 960.56
    elif state_income < 68350:
        state_tax_due = (state_income - 54081) * 0.08 + 1867.88
    elif state_income < 348137:
        state_tax_due = (state_income - 68350) * 0.093 + 3009.4
    elif state_income < 418961:
        state_tax_due = (state_income - 348137) * 0.103 + 29029.591
    else:
        state_tax_due = (state_income - 418961) * 0.113 + 36324.463

    #print("Fed Tax " + str(fed_tax_due) + " " + "State: " + str(state_tax_due))

    agg_tax_due = fed_tax_due + state_tax_due
    #print("Aggregate Tax: " + str(agg_tax_due))
    
    return agg_tax_due

