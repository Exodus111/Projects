#!/usr/bin/python3

flat_tax_rate = 50
ubi = 15000

def calculate_ubi_rates(income):
    taxes_owed = int(income*(flat_tax_rate/100))
    taxed_income = int(income - taxes_owed)
    taxes_with_ubi_deducted = int(taxed_income - ubi)
    final_income = int(taxed_income + ubi)
    return "Income: {} \nTaxes Owed: {} \nTaxed Income: {} \nTaxes wth UB deducted: {} \nFinal Income: {}\n\n".format(income, taxes_owed, taxed_income, taxes_with_ubi_deducted, final_income)

def calculate_reverse_taxation(income, lowest_rate=30000):
    if income > lowest_rate:
        taxes_owed = int(income*(flat_tax_rate/100))
    else:
        difference = lowest_rate - income


with open("taxrates.txt", "w+") as f:
    f.write("Flat Tax Rate: "+ str(flat_tax_rate))
    f.write("\n")
    f.write("Universial Basic Income: "+ str(ubi))
    f.write("\n\n")
    for i in range(0, 10000000, 10000):
        f.write(calculate_ubi_rates(i))
