# Script attached to the article "A Security Model for Randomization-based Protected Caches",
#   by Jordi Ribes-Gonzalez, Oriol Farras, Carles Hernandez, Vatistas Kostalabros, and
#   Miquel Moreto.
#
# Corresponding author: Jordi Ribes-Gonzalez (jordi.ribes@urv.cat)
#
# Description: This script computes a number of epochs R and a rekeying period N so that an 
#   RPC is R-epoch N-access secure with at most a certain advantage, using Propositions 2 and 4. 
#   It maximizes the quantity R*N. More concretely, given
#   * S: The number of cache sets of the cache
#   * a: The associativity of the cache
#   * R1: A maximum number of epochs
#   * Adv_rekey_R1: An advantage so that rekey is known to be
#       (R1,Adv_rekey_R1)-pseudo-random
#   * N1: A maximum number of accesses of each epoch (i.e., a maximum rekeying period)
#   * Adv_rand_N1: An advantage so that the cache randomizer is known to be N1-access
#       secure with advantage at most Adv_rand_N1
#   * Adv_ME: A target advantage, larger than Adv_rekey_R1
#   This script computes R<=R1 and N<=N1 so that:
#   * The associated RPC is R-epoch, N-access secure with advantage at most Adv_ME
#   * The number of accesses R*N where we can enforce security is maximized
#   The output is printed in the file 'rk_multi_optimal.out' and by standard output.

# Import of math package requires recent version of Python, e.g. Python 3.8.10.

import argparse
from argparse import RawDescriptionHelpFormatter
from util import *

#RN: This function performs a binary search to compute a rekeying period N<N1 so that the
#   corresponding  RPC is R-epoch, N-access secure with advantage at most Adv_ME, as per
#   Proposition 4. It also returns the value RN.
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

#RN_opt: This function iterates over all possible values of R, so as to find the rekeying
#  period N that makes the corresponding  RPC is R-epoch, N-access secure with advantage
#  at most Adv_ME, and that maximizes the number R*N of accesses where we can enforce
#  security.
def RN_opt(S,a,R1,Adv_rekey_R,N1,Adv_rand_N1,Adv_ME):
    N_out=0
    RN_out=0
    for R in range(1,min([R1,math.ceil((Adv_ME-Adv_rekey_R)/Adv_rand_N1)])+1,1):
        testbound=RN(S,a,R,Adv_rekey_R,N1,Adv_rand_N1,Adv_ME)
        if testbound[1]>RN_out:
            N_out=testbound[0]
            RN_out=testbound[1]
    return [N_out,RN_out]

#main: Point of execution of the script. This function defines the argument parser, computes
#  output from the provided arguments, and prints the output to stout and to file.
def main():
    # Define argument parser, and input arguments
    parser = argparse.ArgumentParser(description='This script computes a number of epochs R and a rekeying period N so that an \nRPC is R-epoch N-access secure with at most a certain advantage, using \nPropositions 2 and 4. It maximizes the quantity R*N. More concretely, this \nscript computes R<=R1 and N<=N1 so that:\n  * The associated RPC is R-epoch, N-access secure with advantage at most \n    Adv_ME. \n  * The number of accesses R*N where we can enforce security is maximized. \nThe output is printed by standard output and in the file rk_multi_optimal.out. \n\nexample: \n  py rk_multi_optimal.py 16 12288 10 0.00001 80000 0.004 0.05', formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('a', metavar='a', type=int, help='associativity of the cache')
    parser.add_argument('S', metavar='S', type=int, help='number of cache sets')
    parser.add_argument('R1', metavar='R1', type=int, help='a maximum number of epochs')
    parser.add_argument('Adv_rekey_R1', metavar='Adv_rekey_R1', type=float, help='an advantage so that rekey is known to be (R1,Adv_rekey_R1)-pseudo-random')
    parser.add_argument('N1', metavar='N1', type=int, help='a maximum number of accesses of each epoch (i.e., a maximum rekeying period)')
    parser.add_argument('Adv_rand_N1', metavar='Adv_rand_N1', type=float, help='an advantage so that the cache randomizer is known to be N1-access secure with advantage at most Adv_rand_N1')
    parser.add_argument('Adv_ME', metavar='Adv_ME', type=float, help='a target advantage, larger than Adv_rekey_R1')
    parser.usage = parser.format_help()
    # Retrieve arguments from parser
    args = parser.parse_args()
    # Compute the result, and print it to stout and to file
    result=RN_opt(args.S,args.a,args.R1,args.Adv_rekey_R1,args.N1,args.Adv_rand_N1,args.Adv_ME)
    print(result)
    f = open('rk_multi_optimal.out','w')
    f.write("(a="+str(args.a)+", S="+str(args.S)+
      ", R1="+str(args.R1)+
      ", p_rekey_R1="+str(round(args.Adv_rekey_R1,5))+
      ", N'="+str(args.N1)+
      ", p_rand_N'="+str(round(args.Adv_rand_N1,5))+
      ", p_ME="+str(round(args.Adv_ME,3))+
      ") -> [N,R*N]="+str(result)+
      "\n")
    f.flush()
    f.close()

if __name__ == "__main__":
    main()
