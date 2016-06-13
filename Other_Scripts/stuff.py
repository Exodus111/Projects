
price_per_k = 11.99
shipping = 6.99
tax = 1.25
exchange = 10.8

def no_tax(amount):
    cost = price_per_k + shipping
    return amount * cost

def taxed(amount):
    price = amount * price_per_k
    cost = price * tax
    return cost + shipping

def get_cheapest(amount):
    a = no_tax(amount)
    b = taxed(amount)
    return (a * exchange), (b * exchange)


for i in range(1, 100):
    without_tax, with_tax = get_cheapest(i)
    out = "{} Kilo med skatt: {} nok. Uten Skatt: {} nok".format(i, int(with_tax), int(without_tax))
    print(out)


