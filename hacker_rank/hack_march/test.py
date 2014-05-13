from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1))


count = 0;
for i in range(1, 100):
    for k in range(1, i):
        count +=1
        print nCk(i, k);
print count
