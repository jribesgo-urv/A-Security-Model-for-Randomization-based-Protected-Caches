# Script attached to the article "A Security Model for Randomization-based Protected Caches",
#   by Jordi Ribes-Gonzalez, Oriol Farras, Carles Hernandez, Vatistas Kostalabros, and
#   Miquel Moreto.
#
# Corresponding author: Jordi Ribes-Gonzalez (jordi.ribes@urv.cat)
#
# Description: This script realizes Proposition 3. More concretely, given a set of cache
#   parameters a,S, a target advantage Adv, and a noise level rho, this script computes a
#   rekeying period N so that the corresponding RPC with an ideal cache randomizer is N-access
#   secure under noise level rho with advantage at most Adv. The output is printed in the file
#   'rk_single_noise.out' and by standard output.

import argparse
from argparse import RawDescriptionHelpFormatter
from util import *

#N: Given the cache parameters S,a, the advantage Adv, and the noise level rho, this function
#   performs a binary search to return a rekeying period N as per Proposition 1.
def N(S,a,Adv,rho):
    out=0
    t=0
    testbound=0
    while testbound<=Adv:
        t+=1
        testbound=cond_cumulative_dist_sum(2**t,1/S,a,rho)
    out=2**(t-1)
    if t>=2:
        for i in range(t-2,-1,-1):
            if cond_cumulative_dist_sum(out+2**i,1/S,a,rho)<=Adv:
                out+=2**i
    if t==0: out=0
    return out

#main: Point of execution of the script. This function defines the argument parser, computes
#  output from the provided arguments, and prints the output to stout and to file.
def main():
    # Define argument parser, and input arguments
    parser = argparse.ArgumentParser(description='This script realizes Proposition 3. More concretely, given a set of cache \nparameters a,S, a target advantage Adv, and a noise level rho, this script \ncomputes a rekeying period N so that the corresponding RPC with an ideal cache \nrandomizer is N-access secure under noise level rho with advantage at most \nAdv. The output is printed by standard output and in the file \nrk_single_noise.out. \n\nexample: \n  py rk_single_noise.py 16 12288 0.01 0.9',formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('a', metavar='a', type=int, help='associativity of the cache')
    parser.add_argument('S', metavar='S', type=int, help='number of cache sets')
    parser.add_argument('Adv', metavar='Adv', type=float, help='target advantage (denoted p in the article)')
    parser.add_argument('rho', metavar='rho', type=float, help='noise level')
    parser.usage = parser.format_help()
    # Retrieve arguments from parser
    args = parser.parse_args()
    # Compute the result, and print it to stout and to file
    result=N(args.S,args.a,args.Adv,args.rho)
    print(result)
    f = open('rk_single_noise.out','w')
    f.write("(a="+str(args.a)+", S="+str(args.S)+", p="+str(round(args.Adv,3))+", rho="+str(round(args.rho,3))+") -> N="+str(result)+"\n")
    f.flush()
    f.close()

if __name__ == "__main__":
    main()
