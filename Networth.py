from dataStruct import EquityBucket
from dataStruct import Scenario
from dataStruct import calculateSalary
from dataStruct import calculate_net_cash
import dataStruct
from reporting import generateTextReport

# Parametric Inputs
stock_app_nom = 0.10
cap_app_nom = 0.05
rent_inflation_nom = 0.1
inflation = 0.03
T0_investments = 1100000
Scenario_Period = 30 # Number of years we want to run the calculation on
T0_Rent = 2500
T0_HomeVal = 1500000 / 2
T0_Salary = 250000
salary_app_nom = 0.04
monthly_childcare = 3000
monthly_spending = 3000
mortgage_interest_rate = 0.07
work_years = 15
property_tax_rate = 0.0125
prop_maintenance_rate = 0.005




# Derived Inputs
cap_app_real = cap_app_nom - inflation
stock_app_real = stock_app_nom - inflation
rent_inflation_real = rent_inflation_nom - inflation
salary_app_real = salary_app_nom - inflation

budget = (T0_Rent + monthly_childcare + monthly_spending) * 12

#salaries, taxes = calculateSalary(T0_Salary, salary_appreciation_real, work_years)

# ============ Scenario Implementation

# Rent Scenario ===============================================================
rent_budget = (T0_Rent + monthly_childcare + monthly_spending) * 12

RentInvestments = EquityBucket(T0_investments, stock_app_real, Period = Scenario_Period, name = "Rent Investments")

rent_net_investments1 = calculate_net_cash(T0_Salary, salary_app_real, rent_budget, 0, Scenario_Period, time_range = (0,7))
rent_net_investments2 = calculate_net_cash(0, salary_app_real, rent_budget, 0, Scenario_Period, time_range = (7,31))
RentInvestments.addInvestmentList(rent_net_investments1)
RentInvestments.addInvestmentList(rent_net_investments2)


RentInvestments.updateEquityValues()
RentScenario = Scenario(Period = Scenario_Period)
RentScenario.addEquity(RentInvestments)
RentScenario.calculateNW()

# Buy Scenario =================================================================
buy_budget = (monthly_childcare + monthly_spending) * 12

BuyScenario = Scenario(Period = Scenario_Period)
BuyInvestments = EquityBucket(T0_investments, stock_app_real, Period = Scenario_Period, name = "Buy Scenario Investments")
BuyInvestments.adjustCash(0, T0_HomeVal * -0.2)


#Create an Equity for the home, pay the down payment, generate the mortgage, and calculate the values
PrimaryHome = EquityBucket(T0_HomeVal, cap_app_real, name = "Home Equity")
PrimaryHome.generateMortgage(mortgage_interest_rate, T0_HomeVal*0.8)
PrimaryHome.updateEquityValues()

# Define Recurring Home Expenses
T0_Home_Tax = T0_HomeVal * property_tax_rate
T0_Maintenance = T0_HomeVal * prop_maintenance_rate # Home Maintenance costs appreciate with real home value
BuyInvestments.addRecurringExpense(T0_Home_Tax, 0.01 , time_range = (0,30)) # Prop tax capped at 1% due to Prop 13
BuyInvestments.addRecurringExpense(T0_Maintenance, cap_app_real, time_range = (0,30))

# Define budgets and investment balances for Buy Scenariod
buy_budget1 = (PrimaryHome.mortgage.monthly_payment + monthly_childcare + monthly_spending) * 12
buy_budget2 = (monthly_childcare + monthly_spending) * 12
buy_cash_balance1 = calculate_net_cash(T0_Salary, salary_app_real, buy_budget1, 0, Scenario_Period, time_range = (0,7))
buy_cash_balance2 = calculate_net_cash(0, salary_app_real, buy_budget1, 0, Scenario_Period, time_range = (7,30))

BuyInvestments.addInvestmentList(buy_cash_balance1)
BuyInvestments.addInvestmentList(buy_cash_balance2)


BuyInvestments.updateEquityValues()

# Add Investments and home equity to Buy Scenario
BuyScenario.addEquity(PrimaryHome)
BuyScenario.addEquity(BuyInvestments)


# Compare Scenarios

BuyScenario.plotScenario()

query_year = 5

# Calculate some final shelter costs for the final report
final_mortgage_payment = PrimaryHome.mortgage.monthly_payment/((1 + inflation) ** query_year)
print(final_mortgage_payment)
final_maintenance = T0_Maintenance / 12 * (1 + prop_maintenance_rate) ** query_year
print(final_maintenance)
final_home_tax = T0_Home_Tax / 12 * (1 + cap_app_real) ** query_year
print(final_home_tax)
final_shelter_cost = final_mortgage_payment + final_maintenance + final_home_tax

generateTextReport(BuyScenario, BuyInvestments, "Buy Scenario", inflation, property=PrimaryHome, year = query_year, home_expenses = final_shelter_cost)

'''
print("Rent Scenario Net Worth: " + str("${0:6,.0f}".format(RentScenario.NW[year])))
print("Rent Scenario Liquid Investments: " + str("${0:6,.0f}".format(RentInvestments.valuations[year])))
print("Rent Scenario 4% Withdrawals: " + str("${0:6,.0f}".format(RentInvestments.valuations[year]*.04)))
'''

'''
print("Home Value: " + str("${0:6,.0f}".format(PrimaryHome.valuations[-1])))
print("Investment Valuations " + str("${0:6,.0f}".format(RentInvestments.valuations[-1])))
'''

''' To Do List
- Add in the tax deductions for mortgage interest
- Adjust scenario so that home ownership doesn't start year 1
- figure out how to easily calculate spending outflows / budgets within investments equities, for reporting
'''
