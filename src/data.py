sql = [("Cash and cash equivalents", "SELECT cash_and_equiv FROM table_name"),
("Short-term investments", "SELECT short_term_invest FROM table_name"),
("Accounts receivable - net", "SELECT net_account_receiv FROM table_name"),
("Inventory", "SELECT inventory FROM table_name"),
("Supplies", "SELECT supplies FROM table_name"),
("Total current assets", "SELECT total_current_assets FROM table_name"),
("Investments", "SELECT investments FROM table_name"),
("Land", "SELECT land FROM table_name"),
("Land improvements", "SELECT land_improvements FROM table_name"),
("Buildings", "SELECT buildings FROM table_name"),
("Equipment", "SELECT equipment FROM table_name"),
("Less: accumulated depreciation", "SELECT accumulated_depreciation FROM table_name"),
("Property, plant & equip. - net", "SELECT net_property FROM table_name"),
("Goodwill", "SELECT goodwill FROM table_name"),
("Other intangible assets", "SELECT other_intangible_assets FROM table_name"),
("Total intangible assets", "SELECT total_intangible_assets FROM table_name"),
("Other assets", "SELECT other_assets FROM table_name"),
("Total assets", "SELECT total_assets FROM table_name"),]

def getsql():
    return sql