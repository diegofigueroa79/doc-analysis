sql = [("Cash and cash equivalents ", "SELECT cash_and_equiv FROM table"),
("Short-term investments ", "SELECT short_term_invest FROM table"),
("Accounts receivable - net ", "SELECT net_account_receiv FROM table"),
("Inventory ", "SELECT inventory FROM table"),
("Supplies ", "SELECT supplies FROM table"),
("Total current assets ", "SELECT total_current_assets FROM table"),
("Investments ", "SELECT investments FROM table"),
("Land ", "SELECT land FROM table"),
("Land improvements ", "SELECT land_improvements FROM table"),
("Buildings ", "SELECT buildings FROM table"),
("Equipment ", "SELECT equipment FROM table"),
("Less: accumulated depreciation ", "SELECT accumulated_depreciation FROM table"),
("Property, plant & equip. - net ", "SELECT net_property FROM table"),
("Goodwill ", "SELECT goodwill FROM table"),
("Other intangible assets ", "SELECT other_intangible_assets FROM table"),
("Total intangible assets ", "SELECT total_intangible_assets FROM table"),
("Other assets ", "SELECT other_assets FROM table"),
("Total assets ", "SELECT total_assets FROM table"),
("Short-term loans payable ", "SELECT short_term_loans_payable FROM table"),
("Current portion of long-term debt ", "SELECT current_long_term_debt FROM table"),
("Accounts payable ", "SELECT accounts_payable FROM table"),
("Accrued compensation and benefits ", "SELECT accrued_comp_benefits FROM table"),
("Income taxes payable ", "SELECT income_taxes_payable FROM table"),
("Other accrued liabilities ", "SELECT other_liabilities FROM table"),
("Deferred revenues ", "SELECT deferred_revenues FROM table"),
("Total current liabilities ", "SELECT total_current_liabilities FROM table"),
("Notes payable ", "SELECT notes_payable FROM table"),
("Bonds payable ", "SELECT bonds_payable FROM table"),
("Deferred income taxes ", "SELECT deferred_income_taxes FROM table"),
("Total long-term liabilities ", "SELECT total_longterm_liabilities FROM table"),
("Total liabilities ", "SELECT total_liabilities FROM table"),
("Common stock ", "SELECT common_stock FROM table"),
("Retained earnings ", "SELECT retained_earnings FROM table"),
("Accum other comprehensive income ", "SELECT other_comp_income FROM table"),
("Less: Treasury stock ", "SELECT treasury_stock FROM table"),
("Total stockholders' equity ", "SELECT total_stockholders_equity FROM table"),
("Total liabilities & stockholders' equity ", "SELECT total_liabilities_stockholders_equity FROM table"),]

def getsql():
    return sql