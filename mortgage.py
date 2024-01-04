

class mortgage:

    def __init__(self, interest_rate, T0_loan_amt, app_rate):
        self.interest_rate = interest_rate
        self.T0_loan_amt = T0_loan_amt
        self.app_rate = app_rate
        self.annual_liabilities_list = [] # Annual list for outstanding liabilities on mortgage
        self.monthly_interest_list = [] # List of monthly interest payments
        self.yearly_interest_list = [] # List of yearly interest payments
        
        # Derived values associated with this mortgage
        self.monthy_int_rate = interest_rate / 12
        self.monthly_payment = (self.monthy_int_rate * T0_loan_amt * (1 + self.monthy_int_rate) ** 360) / ((1 + self.monthy_int_rate) ** 360 - 1)

    def generate_mortgage_schedule(self):
        #Method to generate the mortgage schedule, and set the following:
        
        month = 0
        balance = self.T0_loan_amt
        monthly_balances = []
        monthly_balances.append(balance)
        self.monthly_interest_list.append(balance * self.monthy_int_rate)


        # Generate monthly values for interest paid, liabilities, and remaining balance
        while month < 360:
            monthly_interest = balance * self.monthy_int_rate
            self.monthly_interest_list.append(monthly_interest)
            #print("Adding for month:  " + str(month))
            balance = balance - (self.monthly_payment - monthly_interest)
            monthly_balances.append(balance)
            #print("Month " + str(month) + ": $" + str(monthly_interest))
            month = month + 1


        year = 0
        self.annual_liabilities_list.append(self.T0_loan_amt)

        # Add up the yearly interest payments, and record the end-of-year liabilites and balances
        while year < 30:
            yearly_val = 0
            month = 0
            while month <= 12:
                current_month = (year) * 12 + month
                #print("Current Month is " + str(current_month))
                yearly_val = yearly_val + self.monthly_interest_list[current_month]
                if month == 11: # At the end of the year, record the remaining liability
                    self.annual_liabilities_list.append(monthly_balances[current_month])
                month = month + 1
            #print("Yearly Interest for year: " + str(year) + " " + str(yearly_val))
            self.yearly_interest_list.append(yearly_val)
            year = year + 1
            
        # Append a value of 0 to the annual liabilities list, to pad the final 30th year
        #self.annual_liabilities_list.append(0)
