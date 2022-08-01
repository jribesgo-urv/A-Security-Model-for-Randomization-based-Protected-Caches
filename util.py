# Script attached to the article "A Security Model for Randomization-based Protected Caches",
#   by Jordi Ribes-Gonzalez, Oriol Farras, Carles Hernandez, Vatistas Kostalabros, and
#   Miquel Moreto.
#
# Corresponding author: Jordi Ribes-Gonzalez (jordi.ribes@urv.cat)
#
# Description: Auxiliary functions to the rest of scripts (rk_*.py). The functions herein 
#   compute the cumulative distribution functions used in the article.

# Import of math package requires a recent version of Python, e.g. Python 3.8.10.
import math

#cumulative_dist_sum: Evaluates the cumulative distribution function of the binomial random 
#   variable with parameters n and 1-p at n-k.
def cumulative_dist_sum(k,n,p):
    SUMi=1
    for i in range(0,k,1):
        SUMi-=math.comb(n,i)*(p**i)*((1-p)**(n-i))
    return SUMi

#cond_cumulative_dist_sum: Evaluates the sum of the left-hand side of the inequality of Proposition 3, for p=1/S.
def cond_cumulative_dist_sum(N,p,a,rho):
    SUMi=0
    for i in range(0,a,1):
        SUMj=0
        if a-i<=N-math.floor(rho*N):
            for j in range(0,a-i,1):
                SUMj+=math.comb(N-math.floor(rho*N),j)*(p**j)*((1-p)**(N-math.floor(rho*N)-j))
        if a-i>N-math.floor(rho*N):
            SUMj=1
        SUMi+=math.comb(math.floor(rho*N),i)*(p**i)*((1-p)**(math.floor(rho*N)-i))*(1-SUMj)
    return SUMi