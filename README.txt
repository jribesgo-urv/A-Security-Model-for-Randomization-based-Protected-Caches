Artifacts attached to the article "A Security Model for Randomization-based Protected Caches", by Jordi Ribes-González, Oriol Farràs, Carles Hernández, Vatistas Kostalabros, and Miquel Moretó.

1) Dependencies required to build and run the artifact, including specific version numbers of dependencies

  All scripts require a new version math Python package to compute binomial coefficients, floor and ceil functions. 
  This package is available in Python 3.8.10 and above.

2) Instructions for building and running the artifact

  All four scripts can be run with python, and parameters must be provided as arguments. 
  The description of the scripts and the instructions to launch them can be retrieved with a parameterless execution, or by providing the option '-h'.
  The following is a list of the scripts and their argument names.
    rk_single.py [-h] a S Adv
	rk_single_noise.py [-h] a S Adv rho
	rk_multi_fixed.py [-h] a S R Adv_rekey_R N1 Adv_rand_N1 Adv_ME
	rk_multi_optimal.py [-h] a S R1 Adv_rekey_R1 N1 Adv_rand_N1 Adv_ME
  For example,
    py rk_single.py 16 12288 0.01
  Output is both printed by standard output, and it is also stored in the corresponding '.out' file:
    cat rk_single.out

3) Options on configuring the artifact to run in different modes, if applicable

  Input parameters should be provided as arguments. No further action is needed to configure the artifact.

4) Instructions on how to interpret the output of the artifact, including which scripts to run if appropriate

  Given a set of cache and security parameters, the scripts output the rekeying periods (and number of epochs, in the case of rk_multi_*.py) given by our results by standard output.
  The scripts also print the results to a corresponding file, in the form:
    (cache and security parameters) -> output
  For instance,
    (a=16, S=12288, p=0.01) -> N=100532
	
5) An explanation of how the source code is organized

  Four scripts are provided:
    * rk_single.py: Realizes Proposition 1. Given a set of cache parameters a,S and a target advantage Adv, this script computes a rekeying period N so that the corresponding RPC with an ideal cache randomizer is N-access secure with advantage at most Adv.
	* rk_single_noise.py: Realizes Proposition 3, which is the same than rk_single.py but in the noise setting.
	* rk_multi_fixed.py: Realizes Proposition 2 and 4. Starting with a fixed number of epochs R, this script computes rekeying period N so that an RPC is R-epoch N-access secure with at most a certain advantage.
	* rk_multi_optimal.py: Realizes Proposition 2 and 4. Computes a number of epochs R and a rekeying period N so that an RPC is R-epoch N-access secure with at most a certain advantage, maximizing the number of accesses R*N where security is enforced.
  The source file of the scripts begins with the definition of local functions that compute the output given the input parameters. Next, a main() function defines the argument parser for the command-line execution, followed by a call to the previous functions, and the calls to print to file and to standard output. 
  Common auxiliary functions, such as the cumulative binomial distribution function, are imported from a 'util.py' source file.
  
6) Inputs to verify reported numbers

  We list the (bash) command-line calls to verify the numerical results in the paper.
  
  * Figure 5 (page 13):
      for loga in {0..4}; 
      do for logS in {5..14}; 
      do N=$(py rk_single.py $((2**$loga)) $((2**logS)) 0.01); 
      logN=$(echo $N | awk '{print log($1)/log(2)}'); 
      echo "a=$((2**$loga)) logS=$logS logN=$logN"; 
      done; 
      done;
  
  * First paragraph of Section 5.1:
      py rk_single.py 16 12288 0.01
  
  * Second paragraph of Section 5.1:
      py rk_single_noise.py 16 12288 0.01 0.9
      py rk_single_noise.py 16 12288 0.1 0.9
	
  * Fourth paragraph of Section 5.1:
      py rk_single.py 16 12288 0.000999
      py rk_multi_fixed.py 16 12288 10 0.00001 78705 0.004 0.05
  
  * Fifth paragraph of Section 5.1:
      py rk_single.py 16 12288 0.0000999
      py rk_multi_fixed.py 16 12288 100 0.00001 63486 0.0004 0.05
	
7) Code to verify the simulation results in Section 5

  Our results can be verified using the provided patch on ChampSim, 
  and following the instructions in the README contained therein.
    1) git clone https://github.com/ChampSim/ChampSim.git
    2) git apply random_placement_with_rekey_period.patch