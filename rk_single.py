# Script attached to the article "A Security Model for Randomization-based Protected Caches",
#   by Jordi Ribes-Gonzalez, Oriol Farras, Carles Hernandez, Vatistas Kostalabros, and
#   Miquel Moreto.
#
# Corresponding author: Jordi Ribes-Gonzalez (jordi.ribes@urv.cat)
#
# Description: This script realizes Proposition 1. More concretely, given a set of cache
#   parameters a,S and a target advantage Adv, this script computes a rekeying period N so
#   that the corresponding RPC with an ideal cache randomizer is N-access secure with
#   advantage at most Adv. The output is printed in the file 'rk_single.out' and by standard
#   output.

import argparse
from argparse import RawDescriptionHelpFormatter
from util import *

#N: Given the cache parameters S,a and the advantage Adv, this function performs a binary
#   search to return a rekeying period N as per Proposition 1.
def N(S,a,Adv):
    out=0
    t=0
    testbound=0
    while testbound<=Adv:
        t+=1
        testbound=cumulative_dist_sum(a,2**t,1/S)
    out=2**(t-1)
    if t>=2:
        for i in range(t-2,-1,-1):
            if cumulative_dist_sum(a,out+2**i,1/S)<=Adv:
                out+=2**i
    if t==0: out=0
    return out

#main: Point of execution of the script. This function defines the argument parser, computes
#  output from the provided arguments, and prints the output to stout and to file.
def main():
    # Define argument parser, and input arguments
    parser = argparse.ArgumentParser(description='This script realizes Proposition 1. Given a set of cache parameters a, S and a \ntarget advantage Adv, this script computes a rekeying period N so that the \ncorresponding RPC with an ideal cache randomizer is N-access secure with \nadvantage at most Adv. The result is printed by standard output and in \nthe file rk_single.out. \n\nexample: \n  py rk_single.py 16 12288 0.01',formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('a', metavar='a', type=int, help='associativity of the cache')
    parser.add_argument('S', metavar='S', type=int, help='number of cache sets')
    parser.add_argument('Adv', metavar='Adv', type=float, help='target advantage (denoted p in the article)')
    parser.usage = parser.format_help()
    # Retrieve arguments from parser
    args = parser.parse_args()
    # Compute the result, and print it to stout and to file
    result=N(args.S,args.a,args.Adv)
    print(result)
    f = open('rk_single.out','w')
    f.write("(a="+str(args.a)+", S="+str(args.S)+", p="+str(round(args.Adv,3))+") -> N="+str(result)+"\n")
    f.flush()
    f.close()

if __name__ == "__main__":
    main()
