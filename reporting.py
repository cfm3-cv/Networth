

def generateTextReport(Scenario, LiquidInvestments, Name, inflation, property=None, year = 10, home_expenses = 0, budget = 0):
    
    print('\n')
    print("=========== Final Report for: " + Name + " ===========")
    print("Data reported for Year: " + str(year))
    print("Net Worth: " + str("${0:6,.0f}".format(Scenario.NW[year])))

    print("Liquid Investments: " + str("${0:6,.0f}".format(LiquidInvestments.valuations[year])))
    print("4% Withdrawals: " + str("${0:6,.0f}".format(LiquidInvestments.valuations[year]*.04)))

    final_mortgage_payment = property.mortgage.monthly_payment/((1 + inflation) ** year)
    print("Final Shelter Cost: " + str("${0:6,.0f}".format(home_expenses)))
    print("Other annual Costs: " + "${0:6,.0f}".format(budget))
    print("Total expenses: " + "${0:6,.0f}".format(budget + home_expenses))

    print("========================================================")
    print('\n')

