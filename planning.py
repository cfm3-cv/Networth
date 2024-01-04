'''Planning Document

Class EquityBucket:
    Class buckets of equity, upon which operations can be made
    These objects can contain various cash flow objects
    
Class CashflowAdjustment:
    Dictionary which contains a series of cashflow

What does the flow look like to update the valuation of an equity bucket?
    - Look through the list of cash flow adjustments
    - Each cashflow adjustment will have different rules for updating valuation.
        - Example:
            "Update appreciation" will look at the previous valuation, and apply app value
            "Add Cash" will add money into investments, for example from yearly salary
            "Remove Cash" will remove cash, for example a downpayment
            "Pay Taxes" will *remove* value to invesments, as it's saved on taxes
                - Maybe have an "adjust taxes" function for tax deductions etc.
                
                
Look at the tax one (maybe most complicated?)
- This is done annually, so the EquityBucket will need to be updated regularly
- This needs access to salary data to be calculated
- Deducted (mortgage interest?) is a function to be performed on this

Taxes should be a class, with following functionality:
- Attribute for cash values to be stored each year, and deducted from investments
- Function for adjusting the value, based on things like mortgage interest deductions

Perhaps EquityBucket can have a "pay_taxes" function, which take a "taxes object" as an argument

Overall approach
- EquityBucket will have functions to update various cashflows, and also contain cashflow objects to make these adjustments:
    - Objects that EquityBucket will contain
        - Valuations (simple list)
        - Taxes cashflow object
        - AddCash
            - Will have a dictionary of {year, value}
        - Remove Cas
            - Will have a dictionary of {year, value}
    - Functions for EquityBucket
        - addCashFlowObj function, to add cash flows objects to this EquityBucket instance
        - UpdateValuation, which will do an annual update to its own value list
            - Will use CashFlowObjects to make adjustments
            - Will use equityAppreciation rates for value appreciation



Refactor 12/27/23

- NumPy arrays to contain dollar amounts for certain Equities:
    - Investments (stocks)
    - Home Values (RE)
    - Salary (cash)
    
- NumPy arrays for Outflows / Expenditures
    - Spending (negative cash)
    - Taxes (negative cash)
        - State / Federal Income, Mortgage Writeoffs etc
        
- One-off Operations that can be performed
    - Downpayment on House
    - Inheritance
    
Each NumPy array will be a 2d Array
    - One column for yearly index
    - Next column for financial value


