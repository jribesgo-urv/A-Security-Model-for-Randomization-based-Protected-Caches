# Script attached to the article "A Security Model for Randomization-based Protected Caches",
#   by Jordi Ribes-Gonzalez, Oriol Farras, Carles Hernandez, Vatistas Kostalabros, and
#   Miquel Moreto.
#
# Corresponding author: Jordi Ribes-Gonzalez (jordi.ribes@urv.cat)
#
# Description: This script computes rekeying period N so that an RPC is R-epoch N-access
#   secure with at most a certain advantage, using Propositions 2 and 4. More concretely, 
#   given
#   * S: The number of cache sets of the cache
#   * a: The associativity of the cache
#   * R: A fixed-beforehand number of epochs
#   * Adv_rekey_R: An advantage so that rekey is known to be
#       (R,Adv_rekey_R)-pseudo-random
#   * N1: A maximum number of accesses of each epoch
#   * Adv_rand_N1: An advantage so that the cache randomizer is known to be N1-acccess
#       secure with advantage at most Adv_rand_N1.
#   * Adv_ME: A target advantage, larger than Adv_rekey_R
#   This script returns N<=N1 so that the associated RPC is R-epoch, N-access secure
#   with advantage at most Adv_ME. The output is printed in the file 'rk_multi_fixed.out'
#   and by standard output.

import argparse
from argparse import RawDescriptionHelpFormatter
from util import *

#RN: Given the input to this script, this function performs a binary search to compute
#   a rekeying period N so that the corresponding  RPC is R-epoch, N-access secure
#   with advantage at most Adv_ME, as per Proposition 4. It also returns the value RN.
def RN(S,a,R,Adv_rekey_R,N1,Adv_rand_N1,Adv_ME):
    out=0
    t=0
    testbound=0
    while testbound<=Adv_ME and 2**t<=N1:
        t+=1
        testbound=Adv_rekey_R+R*(cumulative_dist_sum(a,2**t,1/S)+Adv_rand_N1)
    out=2**(t-1)
    if t>=2:
        for i in range(t-2,-1,-1):
            if Adv_rekey_R+R*(cumulative_dist_sum(a,out+2**i,1/S)+Adv_rand_N1)<=Adv_ME and out+2**i<=N1:
                out+=2**i
    if t==0: out=0
    return [out,R*out]

#main: Point of execution of the script. This function defines the argument parser, computes
#  output from the provided arguments, and prints the output to stout and to file.
def main():
    # Define argument parser, and input arguments
    parser = argparse.ArgumentParser(description='This script computes rekeying period N so that an RPC is R-epoch N-access \nsecure with at most a certain advantage, using Propositions 2 and 4. More \nconcretely, this script returns N<=N1 so that the associated RPC is R-epoch, \nN-access secure with advantage at most Adv_ME. The output is printed by \nstandard output and in the file rk_multi_fixed.out. \n\nexample: \n  py rk_multi_fixed.py 16 12288 10 0.00001 80000 0.004 0.05',formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('a', metavar='a', type=int, help='the associativity of the cache')
    parser.add_argument('S', metavar='S', type=int, help='number of cache sets')
    parser.add_argument('R', metavar='R', type=int, help='a fixed-beforehand number of epochs')
    parser.add_argument('Adv_rekey_R', metavar='Adv_rekey_R', type=float, help='an advantage so that rekey is known to be (R,Adv_rekey_R)-pseudo-random')
    parser.add_argument('N1', metavar='N1', type=int, help='a maximum number of accesses of each epoch')
    parser.add_argument('Adv_rand_N1', metavar='Adv_rand_N1', type=float, help='an advantage so that the cache randomizer is known to be N1-access secure with advantage at most Adv_rand_N1.')
    parser.add_argument('Adv_ME', metavar='Adv_ME', type=float, help='a target advantage, larger than Adv_rekey_R')
    parser.usage = parser.format_help()
    # Retrieve arguments from parser
    args = parser.parse_args()
    # Compute the result, and print it to stout and to file
    result=RN(args.S,args.a,args.R,args.Adv_rekey_R,args.N1,args.Adv_rand_N1,args.Adv_ME)
    print(result)
    f = open('rk_multi_fixed.out','w')
    f.write("(a="+str(args.a)+", S="+str(args.S)+
      ", R="+str(args.R)+
      ", p_rekey_R="+str(round(args.Adv_rekey_R,5))+
      ", N'="+str(args.N1)+
      ", p_rand_N'="+str(round(args.Adv_rand_N1,5))+
      ", p_ME="+str(round(args.Adv_ME,3))+
      ") -> [N,R*N]="+str(result)+
      "\n")
    f.flush()
    f.close()


if __name__ == "__main__":
    main()
