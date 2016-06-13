"""Probably naive implementation of: http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
"""

default_top = 100000

while True:
    try:
        top = raw_input("Primes through [default: %s] " % default_top)
        top = int(top) if top else default_top
        if top <= 1: 
            raise ValueError()
        else:
            break
    except ValueError:
        print "Please type an integer > 1"

candidates = range(2, top+1)
primes = []
while candidates:
    print "Processing, candidates remaining:", len(candidates)
    # assertion that the 0th number in any loop is our prime.
    prime = candidates.pop(0)
    primes.append(prime)
    candidates = filter(lambda n: n % prime, candidates)
    
print "Found numbers:"
for prime in primes:
    print prime